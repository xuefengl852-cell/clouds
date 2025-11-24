import logging
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import ClassVar, Dict, Optional

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, InvalidElementStateException, StaleElementReferenceException, \
    NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.config_loader import load_yaml_config

logger = logging.getLogger(__name__)


class BasePage:
    # 按类名缓存的配置字典
    _config_cache: ClassVar[Dict[str, dict]] = {}
    # 每个页面类必须覆盖此属性
    CONFIG_PATH: ClassVar[Optional[str]] = None
    # 项目根目录（根据实际结构调整）
    BASE_DIR = Path(__file__).resolve().parent.parent
    # 定位器类型映射
    LOCATOR_MAPPING = {
        "id": AppiumBy.ID,
        "xpath": AppiumBy.XPATH,
        "class_name": By.CLASS_NAME,
        "css_selector": By.CSS_SELECTOR,
        "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
    }
    
    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> dict:
        """
        加载类缓存，支持类级缓存以及多页面配置
        :param config_path:可选配置文件路径
        :return:配置字典
        """
        final_path = config_path or cls.CONFIG_PATH
        if not final_path:
            # 自动生成默认路径
            class_name = cls.__name__
            snake_case = ''.join(
                ['_' + c.lower() if c.isupper() else c
                 for c in class_name]
            ).lstrip('_').replace('Page', '')
            final_path = f"data/locators/{snake_case}.yaml"
            logger.info(f"自动生成配置路径: {final_path}")
        # 转换为绝对路径
        absolute_path = cls.resolve_config_path(final_path)
        # 检查是否已缓存
        if absolute_path in cls._config_cache:
            return cls._config_cache[absolute_path]
        
        try:
            config = load_yaml_config(absolute_path)
            
            # 确保配置是字典类型
            if not isinstance(config, dict):
                logger.error(f"配置文件内容不是字典: {absolute_path}")
                config = {}  # 返回空字典作为安全值
            
            cls._config_cache[absolute_path] = config
            logger.info(f"已加载配置文件: {absolute_path} (for {cls.__name__})")
            return config
        except Exception as e:
            logger.error(f"加载配置文件失败: {absolute_path} - {e}")
            # 返回空字典避免后续操作失败
            return {}
    
    @classmethod
    def resolve_config_path(cls, path: str) -> str:
        """解析配置文件路径为绝对路径"""
        # 已经是绝对路径直接返回
        if os.path.isabs(path):
            return path
        
        # 基于项目根目录解析
        return str((cls.BASE_DIR / path).resolve())
    
    def __init__(self, driver, platform=None, timeout=10, long_press_duration=2.0, device_id=None):
        """
        :param driver: web drive实例（网盘）
        :param platform: 平台类型（android/ios）
        :param long_press_duration: 长安持续时间（秒）
        :param timeout: 超时时间（秒）
        """
        self.driver = driver
        self.config = self.load_config()
        device_config = self.__class__.load_config()
        # 设置参数实例
        self.platform = platform or device_config.get(
            "platformName", "android"
        ).lower()
        self.timeout = timeout or device_config.get(
            "timeout", 10
        )
        self.long_press_duration = long_press_duration or device_config.get(
            "long_press_duration", 2.0
        )
        self.device_id = device_id or driver.capabilities.get('udid')
        logger.info(f"初始化页面: {self.__class__.__name__} | 平台: {self.platform}")
        self.windows_width = self.driver.get_window_size()['width']
        logger.info(f"当前设备窗口尺寸X为：{self.windows_width}")
        self.windows_height = self.driver.get_window_size()['height']
        logger.info(f"当前设备窗口尺寸Y为：{self.windows_height}")
    
    def _execute_adb(self, command):
        """执行ADB命令（带错误处理）"""
        adb_prefix = f"adb -s {self.device_id}" if self.device_id else "adb"
        full_cmd = f"{adb_prefix} shell {command}"
        
        logger.debug(f"执行ADB命令: {full_cmd}")
        
        try:
            result = subprocess.run(
                full_cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_msg = f"ADB命令失败: {e.stderr.strip()}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
    
    def back(self, retries=3, delay=0.5):
        """可靠的返回键实现"""
        for attempt in range(retries):
            try:
                # 尝试直接使用ADB命令
                self._execute_adb("input keyevent KEYCODE_BACK")
                logger.info("✅ 使用ADB点击返回键")
                return self
            except Exception as e:
                logger.warning(f"返回键尝试 {attempt + 1}/{retries} 失败: {str(e)}")
                if attempt == retries - 1:
                    raise
                time.sleep(delay)
        return self
    
    def _parse_locator(self, locator_str):
        """
        将字符串定位器转换为标准定位元组
        :param locator_str: 定位器字符串 (格式: "type:value")
        :return: (定位类型, 定位值) 元组
        """
        # 处理标准定位格式 (method:value)
        if ':' in locator_str:
            method, value = locator_str.split(':', 1)
            method = method.strip().lower()
            
            # 处理文本定位器
            if method == "text":
                logger.info(f"创建精确文本定位器: '{value.strip()}'")
                return (AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiSelector().text("{value.strip()}")')
            
            if method == "text_contains":
                logger.info(f"创建包含文本定位器: '{value.strip()}'")
                return (AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiSelector().textContains("{value.strip()}")')
            
            if method == "text_matches":
                logger.info(f"创建正则文本定位器: '{value.strip()}'")
                return (AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiSelector().textMatches("{value.strip()}")')
            
            # 处理标准定位类型
            locator_type = self.LOCATOR_MAPPING.get(method)
            if locator_type:
                return locator_type, value.strip()
        
        # 处理完整的资源ID格式 (package:id/name)
        if ':' in locator_str and '/' in locator_str:
            logger.info(f"处理完整资源ID: {locator_str}")
            return By.ID, locator_str
        
        # 默认处理为ID定位
        return By.ID, locator_str
    
    # 读取yaml中的配置数据
    def get_locator(self, section, key):
        """
        从配置中获取定位器
        :param key:第二层键名
        :param section:第三层键名
        :return: 定位器值
        """
        
        try:
            # 获取定位器整个配置部分
            locators_config = self.config.get(
                "locators", {}
            )
            if section in locators_config and key in locators_config[section]:
                locator_value = locators_config[section][key]
                logger.info(
                    f"获取定位器：{section}-{key} = {locator_value}"
                )
                return self._parse_locator(locator_value)
        except Exception as e:
            error_msg = f"获取定位器失败：{section}-{key} = {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def wait_for_element(self, locator, timeout=None, condition='visible'):
        """
        通用等待元素方法
        :param locator: 定位器元组（By，values）
        :param timeout: 超时时间（，秒）
        :param condition: 等待条件（visible/present/clickable）
        :return: WebElement对象
        """
        timeout = timeout or self.timeout
        locator_type, locator_value = locator
        try:
            if condition == 'visible':
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
            elif condition == 'present':
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
            elif condition == 'clickable':
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
            else:
                raise ValueError(f"不支持等待条件：{condition}")
            logger.debug(f"元素定位成功: {locator_type}='{locator_value}'")
            return element
        except TimeoutException:
            error_msg = f"元素定位超时 ({timeout}s): {locator_type}='{locator_value}'"
            logger.error(error_msg)
            return None
        except Exception as e:
            logger.error(f"元素定位异常: {str(e)}")
            # 关键修改：抛出原始异常
            raise
    
    def get_window_size(self):
        """获取窗口尺寸大小"""
        if not hasattr(self, '_window_size') or not self._window_size:
            self._window_size = self.driver.get_window_size()
        return self._window_size
    
    def find_by_text_element(self, text, context_locator=None, timeout=None):
        """
        断言文本在指定上下文中存在
        :param text: 要检查的文本
        :param context_locator: 文本所在的上下文元素定位器 (可选)
        :param timeout: 自定义超时时间 (可选)
        """
        timeout = timeout or self.timeout
        try:
            if context_locator:
                element = self.wait_for_element(context_locator)
                return element
            else:
                # 在整个页面查找文本
                text = WebDriverWait(self.driver, timeout).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, "body"), text),
                    message=f"文本 '{text}' 未在页面中找到"
                )
                return text
        except TimeoutException:
            # 可在此处添加失败截图等操作
            raise AssertionError(f"断言失败: 文本 '{text}' 不存在")
    
    def click(self, locator, condition='clickable', timeout=None):
        # 点击元素
        element = self.wait_for_element(locator, timeout, condition)
        try:
            element.click()
            logger.info(f"点击元素：{locator}")
            return self
        except Exception as e:
            logger.error(f"点击元素失败：{locator}")
            raise
        return self
    
    def input_text(self, locator, text, condition='visible', timeout=None):
        # 输入文本
        element = self.wait_for_element(locator, timeout, condition)
        try:
            element.clear()
            element.send_keys(text)
            logger.info(f"输入文本到 {locator}：'{text}'")
            return text
        except InvalidElementStateException as e:
            logger.error(f"元素不可编辑: {locator}")
            raise
        except Exception as e:
            logger.error(f"输入文本{text}失败: {locator} | {str(e)}")
            raise
    
    def find_by_locator_index(self, locator, index=0, timeout=None):
        """
        通过定位器和索引查找元素
        :param locator: 定位器元组 (By, value)
        :param index: 索引（从0开始）
        :param timeout: 超时时间
        :return: WebElement对象
        """
        # 解构定位器元组
        locator_type, locator_value = locator
        
        # 根据定位器类型构建XPath
        if locator_type == AppiumBy.ID:
            # 处理资源ID定位器
            resource_id = locator_value
            xpath = f'//*[@resource-id="{resource_id}"][{index + 1}]'
            return self.wait_for_element((AppiumBy.XPATH, xpath), timeout)
        
        elif locator_type == AppiumBy.XPATH:
            # 处理XPath定位器 - 添加索引
            # 确保XPath表达式用括号包裹以便添加索引
            if not locator_value.startswith("("):
                xpath = f"({locator_value})[{index + 1}]"
            else:
                xpath = f"{locator_value}[{index + 1}]"
            return self.wait_for_element((AppiumBy.XPATH, xpath), timeout)
        
        elif locator_type == AppiumBy.ANDROID_UIAUTOMATOR:
            # 处理Android UiAutomator定位器 - 添加索引
            uiautomator = locator_value
            # 检查是否已有索引支持
            if "instance(" not in uiautomator:
                # 添加索引支持
                uiautomator = f"{uiautomator}.instance({index})"
            return self.wait_for_element((AppiumBy.ANDROID_UIAUTOMATOR, uiautomator), timeout)
        
        else:
            # 其他定位器类型不支持索引
            logger.warning(f"定位器类型 {locator_type} 不支持索引，将直接使用原始定位器")
            return self.wait_for_element(locator, timeout)
    
    def click_by_locator_index(self, locator, index=0, timeout=None):
        """通过定位器和索引定位元素进行点击"""
        element = self.find_by_locator_index(locator, index, timeout)
        element.click()
        logger.info(f"点击元素：{locator} [索引： {index}]")
    
    def find_by_text(self, text, match='exact', timeout=None):
        """通过文本查找元素"""
        if match == "exact":
            locator = f'new UiSelector().text("{text}")'
        elif match == "contains":
            locator = f'new UiSelector().textContains("{text}")'
        else:
            locator = f'new UiSelector().textMatches("{text}")'
        return self.wait_for_element((AppiumBy.ANDROID_UIAUTOMATOR, locator), timeout)
    
    def click_by_text(self, text, match='exact', timeout=None):
        """通过文本点击元素"""
        element = self.find_by_text(text, match, timeout)
        try:
            element.click()
            logger.info(f"点击文本元素: '{text}' (匹配模式: {match})")
            return True
        except Exception as e:
            logger.error(f"点击文本元素失败: '{text}' | {str(e)}")
            raise
    
    def find_by_id(self, locator, condition='visible', timeout=None):
        try:
            element = self.wait_for_element(locator, timeout, condition)
            logger.info(f"元素已找到：{element}")
            return element
        except TimeoutException as e:
            logger.warning(f"查找元素超时：{e}")
    
    def get_input_value_by_id(self, locator, attribute_name, condition='clickable', timeout=None):
        """
        获取元素属性值
        :param locator:
        :param attribute_name:
        :param condition:
        :param timeout:
        :return:
        """
        try:
            element = self.wait_for_element(locator, timeout, condition)
            value = element.get_attribute(attribute_name)
            logger.info(f"获取当前元素文本值为：{value}")
            return value
        except StaleElementReferenceException:
            logger.warning("元素过时，重新获取")
            # 重新获取元素并重试
            element = self.wait_for_element(locator, timeout)
            return element.get_attribute(attribute_name)
        except Exception as e:
            logger.error(f"获取属性失败: {attribute_name} | 定位器: {locator} | 错误: {str(e)}")
            self.take_screenshot(f"get_attribute_failed_{attribute_name}")
            return None
    
    def get_text_by_id(self, locator, timeout=None, condition="visible"):
        """
        根据元素id获取文本
        :param condition: 定位元素方式
        :param locator: id元组
        :param timeout: 超时时长
        :return: 元素文本值
        """
        try:
            element = self.wait_for_element(locator, timeout, condition)
            return element.text
        except TimeoutException:
            raise logger.error(f"元素 {element} 未在 {timeout} 秒内找到")
        except StaleElementReferenceException:
            # 处理元素过期的异常
            return self.get_text_by_id(element, timeout)
        except Exception as e:
            # 记录其他异常并重新抛出
            raise logger.error(f"获取元素文本失败: {str(e)}")
    
    def take_screenshot(self, name):
        """
        截取屏幕截图并保存
        :param name: 截图名称
        :return: 截图文件路径
        """
        try:
            # 确保截图目录存在
            screenshot_dir = os.path.join(os.getcwd(), "screenshots")
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            # 生成截图文件路径
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
            
            # 截屏
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"截图已保存: {screenshot_path}")
            
            return screenshot_path
        
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None
    
    def long_press(self, locator, duration=None, condition="visible", timeout=None):
        """
        长按元素
        :param locator:
        :param duration:长按时间
        :param condition:元素等待条件
        :param timeout:超时等待
        :return:bool 操作是否成功
        """
        try:
            element = self.wait_for_element(locator, timeout, condition)
            duration = duration or self.long_press_duration
            actions = ActionChains(self.driver)
            (
                actions.w3c_actions
                .pointer_action
                .move_to(element)
                .click_and_hold()
                .pause(duration)
                .release()
            )
            actions.perform()
            logger.info(f"成功长按元素: {locator} ({duration}秒)")
            return True
        except TimeoutException as e:
            logger.error(f"长按操作失败：元素未找到{locator}")
            raise
        except Exception as e:
            logger.error(f"长按操作异常: {locator} | {str(e)}")
            raise
    
    def wait_for_toast(self, message: str) -> bool:
        """
        等待并验证 Toast 出现
        :param message: 预期包含的文本内容
        :return: 是否成功捕获
        """
        if self.platform == "android":
            # Android 使用 XPath 定位
            locator = (AppiumBy.XPATH, f'//android.widget.Toast[contains(@text, "{message}")]')
        elif self.platform == "ios":
            # iOS 使用 Predicate 定位
            locator = (AppiumBy.IOS_PREDICATE, f'label CONTAINS "{message}"')
        else:
            logger.error(f"Unsupported platform: {self.platform}")
            return False
        
        try:
            # 显式等待 + 存在性检查（非可见性）
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            actual_text = element.text
            if message in actual_text:
                logger.info(f"✅ Toast 验证成功 | 预期: '{message}' | 实际: '{actual_text}'")
                return True
            logger.warning(f"⚠️ Toast 文本不匹配 | 预期: '{message}' | 实际: '{actual_text}'")
            return False
        except TimeoutException:
            logger.error(f"❌ Toast 等待超时 ({self.timeout}s) | 内容: '{message}'")
            return False
    
    def get_toast_text(self) -> Optional[str]:
        """
        获取当前显示的 toast 文本
        :return: toast 文本内容，未找到返回 None
        """
        try:
            # Android 原生 toast 处理
            toast_locator = (AppiumBy.XPATH, "//android.widget.Toast")
            toast_element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(toast_locator))
            return toast_element.text
        except Exception as e:
            logger.error(f"异常信息：{e}")
    
    def assert_desktop_visible(self, locators, timeout=None):
        """断言系统桌面可见"""
        
        desktop_indicators = [locators]
        
        for locator in desktop_indicators:
            try:
                self.wait_for_element(locator, timeout)
                logger.info(f"查找元素桌面成功：{locator}")
                return True
            except Exception as e:
                logger.info(f"查找桌面元素失败：{e}")
                continue
    
    def wait_for_elements(self, locator, condition='present', timeout=None):
        """
        等待多个元素满足条件

        :param locator: 元素定位器
        :param condition: 等待条件 ('present', 'visible', 'clickable')
        :param timeout: 超时时间
        :return: 元素列表
        """
        if timeout is None:
            timeout = self.timeout
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            
            if condition == 'present':
                return wait.until(
                    EC.presence_of_all_elements_located(locator)
                )
            elif condition == 'visible':
                return wait.until(
                    EC.visibility_of_all_elements_located(locator)
                )
            elif condition == 'clickable':
                # 对于多个元素，检查所有元素是否可点击
                def _all_elements_clickable(driver):
                    elements = driver.find_elements(*locator)
                    return elements if elements and all(
                        element.is_enabled() and element.is_displayed() for element in elements) else False
                
                return wait.until(_all_elements_clickable)
            else:
                raise ValueError(f"不支持的等待条件: {condition}")
        
        except TimeoutException:
            logger.warning(f"等待元素超时: {locator} | 条件: {condition} | 超时: {timeout}s")
            return []
        except Exception as e:
            logger.error(f"等待元素异常: {locator} | 错误: {str(e)}")
            raise
    
    def get_element_attribute(self, locator, attribute, multiple=False, condition='present'):
        """
        通用获取元素属性值方法 - 支持单元素和多元素

        :param locator: 元素定位器
        :param attribute: 属性名称
        :param multiple: 是否获取多个元素，False-返回单个值，True-返回列表
        :param condition: 等待条件 (默认'present')
        :param timeout: 超时时间
        :param index: 当multiple=False时，指定获取第几个元素的属性
        :return: 单个属性值或属性值列表
        """
        try:
            timeout = self.timeout
            if multiple:
                # 获取多个元素模式
                elements = self.wait_for_elements(
                    locator,
                    condition=condition,
                    timeout=timeout
                )
                
                if not elements:
                    logger.warning(f"未找到任何元素: {locator}")
                    return []
                
                values = []
                for i, element in enumerate(elements):
                    try:
                        value = element.get_attribute(attribute)
                        values.append(value)
                        logger.debug(f"第 {i + 1} 个元素属性 [{attribute}] 值: {value}")
                    except StaleElementReferenceException:
                        logger.warning(f"第 {i + 1} 个元素过时，重新获取...")
                        # 重新获取所有元素
                        refreshed_elements = self.wait_for_elements(locator, timeout=5)
                        if i < len(refreshed_elements):
                            value = refreshed_elements[i].get_attribute(attribute)
                            values.append(value)
                        else:
                            logger.error(f"重新获取后第 {i + 1} 个元素不存在")
                            values.append(None)
                
                return values
            
            else:
                # 获取单个元素模式
                element = self.wait_for_element(
                    locator,
                    condition=condition,
                    timeout=timeout
                )
                value = element.get_attribute(attribute)
                logger.debug(f"元素属性 [{attribute}] 值: {value}")
                return value
        
        except Exception as e:
            error_msg = f"获取属性失败: {attribute} | 定位器: {locator} | 错误: {str(e)}"
            logger.error(error_msg)
            self.take_screenshot(f"get_attribute_failed_{attribute}")
            raise RuntimeError(error_msg)
    
    def assert_password_display_state(self, locator, expected_state, expected_text=None, timeout=None):
        """
        综合断言密码框状态（安全/非安全模式）

        :param locator: 密码框定位器
        :param expected_state: 预期状态 ('plain' 或 'masked')
        :param expected_text: 预期文本（明文状态下需要）
        :param timeout: 超时时间
        """
        timeout = timeout or self.timeout
        # 获取密码框安全状态属性
        is_password = self.get_element_attribute(
            locator,
            attribute='password',
            condition='clickable',
            timeout=timeout
        )
        
        if expected_state == 'plain':
            # 验证当前是否为明文状态
            if is_password != 'false':
                raise AssertionError(
                    f"密码框应为明文状态 | 实际安全状态: {is_password}"
                )
            logger.info("密码框明文状态断言成功")
            
            # 验证文本内容
            if expected_text is not None:
                actual_text = self.get_element_attribute(
                    locator,
                    attribute='text',
                    timeout=timeout
                )
                assert actual_text == expected_text, (
                    f"明文内容不匹配\n预期: {expected_text}\n实际: {actual_text}"
                )
        
        elif expected_state == 'masked':
            # 验证当前是否为掩码状态
            if is_password != 'true':
                raise AssertionError(
                    f"密码框应为掩码状态 | 实际安全状态: {is_password}"
                )
            logger.info("密码框掩码状态断言成功")
            
            # 验证掩码格式
            actual_text = self.get_element_attribute(locator, "text")
            if not self.is_masked_text(actual_text):
                raise AssertionError(f"文本未正确掩码: {actual_text}")
        
        else:
            raise ValueError(f"无效状态: {expected_state}。只支持 'plain' 或 'masked'")
    
    def assert_password_masked(self, locator, timeout=None):
        """
        快捷验证密码框掩码状态
        """
        self.assert_password_display_state(
            locator,
            expected_state='masked',
            timeout=timeout
        )
        logger.info("密码框掩码状态验证通过")
    
    def assert_password_plain(self, locator, expected_text, timeout=None):
        """
        快捷验证密码框明文状态及内容
        """
        self.assert_password_display_state(
            locator,
            expected_state='plain',
            expected_text=expected_text,
            timeout=timeout
        )
        logger.info(f"密码框明文状态验证通过，内容: {expected_text}")
    
    def is_masked_text(self, text):
        """
        检查文本是否为掩码格式
        """
        if not text:
            return False
        
        # 常见掩码字符：•●*◦·等
        mask_chars = {'•', '●', '*', '◦', '·', '▪', '♦'}
        return all(char in mask_chars for char in text)
    
    def assert_toast(self, message):
        
        """断言 Toast 出现，失败时抛出异常"""
        if not self.wait_for_toast(message):
            raise AssertionError(f"Toast 未检测到: '{message}'")
    
    def assert_text_visible(self, text):
        assert self.find_by_text_element(text), f"断言失败当前元素不存在：{text}"
    
    def assert_element_visible(self, locator, timeout=None):
        """断言元素可见"""
        assert self.wait_for_element(locator, timeout, "visible"), \
            f"元素：{locator}不存在"
        logger.info(f"断言元素可见成功: {locator}")
    
    def get_config_value(self, section, key, default=None):
        """获取配置值"""
        return self.config.get("locators", {}).get(section, {}).get(key, default)
    
    def get_device_config(self, key, default=None):
        """获取设备配置值"""
        return self.config.get("device", {}).get(key, default)
    
    def get_appium_config(self, key, default=None):
        """获取Appium配置值"""
        return self.config.get("appium", {}).get(key, default)
    
    def get_locator_config(self, section, key, default=None):
        """获取定位器配置值"""
        return self.config.get("locators", {}).get(section, {}).get(key, default)
    
    def navigate_to(self, page_class, *args, **kwargs):
        """导航到另一个页面对象"""
        return page_class(self.driver, *args, **kwargs)  # 关键：传递当前driver
    
    def is_resource_id_text_visible(self, locator, text: str, timeout=None):
        """
        通过定位器和索引查找元素
        :param text:
        :param locator: 定位器元组 (By, value)
        :param timeout: 超时时间
        :return: WebElement对象
        """
        timeout = timeout or self.timeout
        # 解构定位器元组
        locator_type, locator_value = locator
        
        try:
            if locator_type == AppiumBy.ID:
                # 处理资源ID定位器
                resource_id = locator_value
                xpath = f'//*[@resource-id="{resource_id}" and @text="{text}"]'
                return self.wait_for_element((AppiumBy.XPATH, xpath), timeout)
        except Exception as e:
            logger.error(f"元素断言异常：{e}")
            return False
    
    def _get_indexed_xpath(self, locator, index):
        """
        根据定位器和索引生成XPath表达式（内部方法）
        :param locator: 定位器元组 (By, value)
        :param index: 索引（从0开始）
        :return: XPath字符串
        """
        locator_type, locator_value = locator
        adjusted_index = index + 1  # 将0-based索引转为1-based
        
        if locator_type == AppiumBy.ID:
            return f'//*[@resource-id="{locator_value}"][{adjusted_index}]'
        elif locator_type == AppiumBy.XPATH:
            return f'({locator_value})[{adjusted_index}]'
        elif locator_type == AppiumBy.CLASS_NAME:
            return f'//*[@class="{locator_value}"][{adjusted_index}]'
        elif locator_type == AppiumBy.ACCESSIBILITY_ID:
            return f'//*[@content-desc="{locator_value}"][{adjusted_index}]'
        else:
            raise ValueError(f"不支持的定位器类型: {locator_type}")
    
    def get_element_by_locator_index(self, locator, index=0, timeout=None):
        """
        通过定位器和索引查找元素
        :param locator: 定位器元组 (By, value)
        :param index: 索引（从0开始）
        :param timeout: 超时时间
        :return: WebElement对象
        """
        timeout = timeout or self.timeout
        xpath = self._get_indexed_xpath(locator, index)
        try:
            # 直接调用 wait_for_element，它会抛出异常
            return self.wait_for_element((AppiumBy.XPATH, xpath), timeout)
        except Exception as e:
            # 添加更多上下文信息
            logger.error(f"按索引获取元素失败: locator={locator}, index={index}")
            # 关键修改：重新抛出异常
            raise
    
    def get_paginated_data(self, page_indicator_locator, section, key, next_button_locator):
        """
        通用分页数据获取方法，并在结束后恢复页面到初始状态

        :param key: 数据键
        :param section: 数据部分
        :param page_indicator_locator: 页码指示器元素定位器
        :param next_button_locator: 下一页按钮定位器
        :return: 所有页面数据的列表
        """
        try:
            all_data = []
            page_info = self.get_element_attribute(page_indicator_locator, "text")
            current_page_str, separator, total_pages_str = page_info.partition('/')
            current_page = int(current_page_str)
            total_pages = int(total_pages_str)
            logger.info(f"当前页: {current_page}, 总页数: {total_pages}")
            
            for page_num in range(current_page, total_pages + 1):
                logger.info(f"正在处理第 {page_num} 页")
                
                page_data = self.get_all_folder_texts(section, key)
                
                if page_data:
                    all_data.extend(page_data)
                    logger.info(f"第 {page_num} 页找到 {len(page_data)} 条数据")
                else:
                    logger.warning(f"第 {page_num} 页没有找到数据")
                
                # 如果不是最后一页，点击下一页
                if page_num < total_pages:
                    self.click(next_button_locator)
                    logger.info("已点击下一页")
                    
                    # 等待页面加载
                    time.sleep(1)  # 根据实际情况调整等待时间
            
            logger.info(f"总共找到 {len(all_data)} 条数据")
            
            return all_data
        except Exception as e:
            logger.error(f"获取分页数据时出错: {str(e)}")
            raise
    
    def get_all_folder_texts(self, section, key):
        """
            获取页面中所有文件夹的文本内容
            :param section: 定位器配置部分
            :param key: 定位器键名
            :return: 文本列表
        """
        try:
            locator = self.get_locator(section, key)
            logger.info(f"使用定位器: {locator}")
            # 查找所有具有相同ID的文件夹元素
            folders = self.driver.find_elements(*locator)
            logger.info(f"找到 {len(folders)} 个文件夹元素")  # 提取每个文件夹的文本
            texts = []
            for folder in folders:
                try:
                    text = folder.get_attribute('text')
                    if text:
                        texts.append(text)
                except StaleElementReferenceException:
                    # 处理元素过时异常
                    continue
            logger.info(f"提取的文件夹文本: {texts}")
            return texts
        except Exception as e:
            logger.error(f"获取文件夹文本失败: {e}")
            return []
    
    def _safe_navigate_back(self, max_attempts=3):
        """安全地导航返回，处理可能的异常"""
        for attempt in range(max_attempts):
            try:
                self.back()
                time.sleep(1)  # 等待页面加载
            except Exception as e:
                logger.error(f"返回异常：{e}")
    
    def navigate_back(self, steps):
        # 公共方法封装内部实现
        self._safe_navigate_back(steps)
    
    def _navigate_to_next_page(self, next_button_locator, click_method, long_press_duration):
        """导航到下一页"""
        if click_method == "click":
            self.click(next_button_locator)
        elif click_method == "long_press":
            self.long_press_element(next_button_locator, long_press_duration)
        
        logger.info(f"已{click_method}下一页")
        
        # 等待页面加载
        time.sleep(2)
    
    def _all_targets_found(self, target_filenames, selected_count):
        """检查是否已找到所有目标文件"""
        # 这个方法需要根据你的具体逻辑实现
        # 这里只是一个示例实现，你可能需要根据实际情况调整
        return selected_count >= len(target_filenames)
    
    def long_press_element(self, element_or_locator, duration=1000):
        """
        长按元素

        :param element_or_locator: 元素对象或定位器
        :param duration: 长按持续时间（毫秒）
        """
        try:
            # 如果传入的是定位器，先找到元素
            if isinstance(element_or_locator, tuple):
                element = self.driver.find_element(*element_or_locator)
            else:
                element = element_or_locator
            
            # 使用W3C Actions实现长按
            from selenium.webdriver.common.action_chains import ActionChains
            from selenium.webdriver.common.actions.action_builder import ActionBuilder
            from selenium.webdriver.common.actions.pointer_input import PointerInput
            from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
            
            # 获取元素位置
            location = element.location
            size = element.size
            x = location['x'] + size['width'] // 2
            y = location['y'] + size['height'] // 2
            
            # 使用你的_tap_w3c_actions方法（如果支持长按）
            if hasattr(self, '_tap_w3c_actions'):
                self._tap_w3c_actions(x, y, duration)
            else:
                # 备用方案：使用ActionChains
                actions = ActionChains(self.driver)
                actions.click_and_hold(element).pause(duration / 1000).release().perform()
        
        except Exception as e:
            logger.error(f"长按元素失败: {e}")
            raise
    
    def _all_targets_found(self, target_filenames, selected_count):
        """
        检查是否已经找到所有目标文件

        :param target_filenames: 目标文件列表
        :param selected_count: 已选择的文件数量
        :return: 是否已找到所有目标文件
        """
        if not target_filenames:  # 如果目标文件列表为空
            return False
        
        # 如果已选择的数量等于目标文件数量，则认为已找到所有文件
        return selected_count >= len(target_filenames)
    
    def identify_popup_type_simple(self):
        """简单识别弹窗类型"""
        try:
            # 获取当前页面结构信息
            page_source = self.driver.page_source.lower()
            window_size = self.driver.get_window_size()
            screen_width = window_size['width']
            screen_height = window_size['height']
            
            # 尝试查找弹窗根元素
            popup_selectors = [
                "//*[contains(@class, 'dialog')]",
                "//*[contains(@class, 'modal')]",
                "//*[contains(@class, 'popup')]",
                "//*[contains(@class, 'sheet')]",
                "//*[contains(@class, 'bottom')]",
                "//*[contains(@resource-id, 'dialog')]",
                "//*[contains(@resource-id, 'modal')]",
                "//*[contains(@resource-id, 'popup')]"
            ]
            
            popup_element = None
            for selector in popup_selectors:
                try:
                    element = self.driver.find_element_by_xpath(selector)
                    if element.is_displayed():
                        popup_element = element
                        break
                except:
                    continue
            
            # 根据特征判断类型
            if popup_element:
                location = popup_element.location
                size = popup_element.size
                
                # 检查位置特征
                if location['y'] + size['height'] > screen_height * 0.7:
                    return "底部弹窗 (Bottom Sheet)"
                elif size['width'] > screen_width * 0.9 and size['height'] > screen_height * 0.9:
                    return "全屏弹窗 (Full Screen)"
                elif "dialog" in page_source or "alert" in page_source:
                    return "对话框 (Dialog)"
                elif "toast" in page_source:
                    return "吐司提示 (Toast)"
                else:
                    return f"未知弹窗 (位置: {location}, 大小: {size})"
            else:
                # 如果没有找到明显的弹窗元素，检查页面变化
                if "选择" in self.driver.page_source or "选项" in self.driver.page_source:
                    return "选择菜单 (Option Menu)"
                else:
                    return "无可见弹窗或弹窗元素未识别"
        
        except Exception as e:
            logger.error(f"识别弹窗类型失败: {e}")
            return f"识别错误: {str(e)}"
    
    def _tap_w3c_actions(self, x, y, duration=None):
        """使用修正后的W3C Actions标准"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            from selenium.webdriver.common.actions.action_builder import ActionBuilder
            from selenium.webdriver.common.actions.pointer_input import PointerInput
            from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
            
            # 创建触摸指针输入
            pointer_input = PointerInput(POINTER_TOUCH, "touch")
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=pointer_input)
            
            # 移动到指定位置
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            # 按下
            actions.w3c_actions.pointer_action.pointer_down()
            
            # 处理持续时间（长按）
            if duration:
                actions.w3c_actions.pointer_action.pause(duration / 1000)
            else:
                actions.w3c_actions.pointer_action.pause(0.1)
            
            # 释放
            actions.w3c_actions.pointer_action.pointer_up()
            # 执行操作
            actions.perform()
        
        except Exception as e:
            print(f"W3C Actions 执行失败: {e}")
            # 可以在这里添加回退方案
            raise
    
    def click_through_coordinates(self, x, y, duration=None):
        self._tap_w3c_actions(x, y, duration)
        logger.info(f"点击坐标：{x}，{y}")
    
    def select_all_click(self, locator):
        """
        全选当前页
        :param locator: 元素
        :return: 全选个数
        """
        try:
            elements = self.wait_for_elements(
                locator=locator,
                condition='clickable'
            )
            logger.info(f"找到 {len(elements)} 个元素，开始逐个点击...")
            clicked_count = 0
            for index, element in enumerate(elements):
                try:
                    # 确保元素可见和可点击
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        clicked_count += 1
                        logger.debug(f"成功点击第 {index + 1} 个元素")
                    else:
                        logger.warning(f"第 {index + 1} 元素不可点击")
                except Exception as e:
                    logger.error(f"点击第 {index + 1} 个元素失败: {str(e)}")
            logger.info(f"成功点击 {clicked_count}/{len(elements)} 个元素")
            return clicked_count
        except Exception as e:
            error_msg = f"点击全部元素失败：{str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def click_based_on_the_file_name(self, root_layout_locator, file_name_locator, checkbox_locator, filenames,
                                     current_page: int, all_pages: int,
                                     next_page_locator=None):
        """
        根据多个文件名点击对应的元素（支持分页查找）

        :param all_pages: 所有页
        :param current_page: 当前页
        :param root_layout_locator: 父定位器
        :param file_name_locator: 文件名称定位器
        :param checkbox_locator: 被点击元素定位器
        :param filenames: 文件名称列表，如 ["file1.pdf", "file2.jpg"]
        :param next_page_locator: 下一页按钮定位器（如无分页可省略）
        :return: 成功点击的文件数量
        """
        success_count = 0
        remaining_filenames = filenames.copy()  # 记录未找到的文件名，避免重复查找
        
        try:
            while remaining_filenames and current_page <= all_pages:
                # 1. 获取当前页的所有文件项
                file_items = self.driver.find_elements(*root_layout_locator)
                logger.info(f"第{current_page}页共有{len(file_items)}个文件项")
                
                # 2. 遍历当前页的文件项，查找剩余目标文件
                for target_filename in list(remaining_filenames):  # 用list避免遍历中修改列表报错
                    found = False
                    for item in file_items:
                        try:
                            name_element = item.find_element(*file_name_locator)
                            current_filename = name_element.text.strip()  # 去除空格，避免匹配误差
                            
                            if current_filename == target_filename:
                                # 找到目标文件，点击复选框
                                checkbox_element = item.find_element(*checkbox_locator)
                                checkbox_element.click()
                                logger.info(f"第{current_page}页：成功点击文件: {target_filename}")
                                success_count += 1
                                remaining_filenames.remove(target_filename)  # 从剩余列表中移除
                                found = True
                                break  # 跳出内层循环，继续下一个目标文件
                        except Exception as e:
                            logger.debug(f"处理第{current_page}页文件项时出错: {e}")
                            continue
                    
                    if not found:
                        logger.debug(f"第{current_page}页未找到文件: {target_filename}")
                
                # 3. 如果还有未找到的文件，且有下一页，执行翻页
                if remaining_filenames and next_page_locator:
                    try:
                        # 点击下一页
                        next_page_btn = self.driver.find_element(*next_page_locator)
                        next_page_btn.click()
                        logger.info(f"翻到第{current_page + 1}页")
                        current_page += 1
                        # 等待新页面加载完成（根据实际页面调整等待时间或条件）
                        self.driver.implicitly_wait(2)  # 简单等待，推荐用WebDriverWait显式等待
                    except Exception as e:
                        logger.warning(f"无法翻到第{current_page + 1}页（可能是最后一页）: {e}")
                        break  # 翻页失败，退出循环
                else:
                    break  # 无下一页或已找到所有文件，退出循环
            
            # 4. 处理未找到的文件
            for filename in remaining_filenames:
                logger.warning(f"所有页面均未找到文件: {filename}")
            
            logger.info(f"总成功点击了 {success_count} 个文件")
            return success_count
        
        except Exception as e:
            logger.error(f"点击多个文件时失败：{e}")
            return success_count
    
    import logging
    
    logger = logging.getLogger(__name__)
    
    def long_press_based_on_the_file_name(self, root_layout_locator, file_name_locator, target_locator, filenames,
                                          current_page: int, all_pages: int,
                                          long_press_duration=2000, next_page_locator=None):
        """
        根据多个文件名长按对应的元素（支持分页查找）

        :param root_layout_locator: 父定位器
        :param file_name_locator: 文件名称定位器
        :param target_locator: 被长按元素定位器
        :param filenames: 文件名称列表，如 ["file1.pdf", "file2.jpg"]
        :param current_page: 当前页（起始页，如1）
        :param all_pages: 总页数（最大翻页上限）
        :param long_press_duration: 长按持续时间（毫秒），默认2000ms
        :param next_page_locator: 下一页按钮定位器（无分页可省略）
        :return: 成功长按的文件数量
        """
        success_count = 0
        remaining_filenames = filenames.copy()  # 记录未找到的文件名，避免重复查找
        actions = ActionChains(self.driver)  # 初始化动作链（复用，提高效率）
        
        try:
            while remaining_filenames and current_page <= all_pages:
                # 1. 获取当前页的所有文件项
                file_items = self.driver.find_elements(*root_layout_locator)
                logger.info(f"第{current_page}页共有{len(file_items)}个文件项")
                
                # 2. 遍历当前页的文件项，查找剩余目标文件
                for target_filename in list(remaining_filenames):  # 用list避免遍历中修改列表报错
                    found = False
                    for item in file_items:
                        try:
                            # 获取当前文件项的文件名
                            name_element = item.find_element(*file_name_locator)
                            current_filename = name_element.text.strip()  # 去除空格，提高匹配精度
                            
                            if current_filename == target_filename:
                                logger.info(
                                    f"对比文件名：目标={target_filename} | 页面实际={current_filename},对比文件名：目标；类型={type(target_filename)} | 页面实际={type(current_filename)}")
                                # 找到目标文件，执行长按操作
                                target_element = item.find_element(*target_locator)
                                actions.click_and_hold(target_element) \
                                    .pause(long_press_duration / 1000) \
                                    .release() \
                                    .perform()
                                
                                logger.info(
                                    f"第{current_page}页：成功长按文件: {target_filename}，持续时间: {long_press_duration}ms")
                                success_count += 1
                                remaining_filenames.remove(target_filename)  # 从剩余列表移除
                                found = True
                                break  # 跳出内层循环，继续下一个目标文件
                        except Exception as e:
                            logger.error(f"处理第{current_page}页文件项时出错: {e}")
                            continue
                    
                    if not found:
                        logger.error(f"第{current_page}页未找到文件: {target_filename}")
                
                # 3. 若还有未找到的文件，且有下一页，执行翻页
                if remaining_filenames and next_page_locator:
                    try:
                        # 点击下一页按钮
                        next_page_btn = self.driver.find_element(*next_page_locator)
                        next_page_btn.click()
                        logger.info(f"翻到第{current_page + 1}页")
                        current_page += 1
                        # 等待新页面加载（推荐用WebDriverWait显式等待，这里简化为隐式等待）
                        self.driver.implicitly_wait(2)
                    except Exception as e:
                        logger.warning(f"无法翻到第{current_page + 1}页（可能是最后一页）: {e}")
                        break  # 翻页失败，退出循环
                else:
                    break  # 无下一页或已找到所有文件，退出循环
            
            # 4. 处理未找到的文件
            for filename in remaining_filenames:
                logger.warning(f"所有页面均未找到文件: {filename}")
            
            logger.info(f"总成功长按了 {success_count} 个文件")
            return success_count
        
        except Exception as e:
            logger.error(f"长按多个文件时失败：{e}")
            return success_count
    
    def get_file_attributes(self, root_layout_locator, file_name_locator, attribute_locator, filenames,
                            current_page: int, all_pages: int, attribute, next_page_locator=None):
        """
        根据文件名列表获取对应文件的属性（支持分页查找）
        :param root_layout_locator: 父容器定位器（元组，如("xpath", "//div[@class='file-list']")）
        :param file_name_locator: 文件名元素定位器（元组，如("id", "name_tv")）
        :param attribute_locator: 目标属性元素定位器（元组，如("id", "info_tv")）
        :param filenames: 文件名列表（如["file1.pdf"]）或单个文件名（如"file1.pdf"）
        :param current_page: 当前起始页（int，如1）
        :param all_pages: 最大翻页上限（int，如5）
        :param attribute: 要获取的属性名（如"text"、"resourceId"）
        :param next_page_locator: 下一页按钮定位器（元组，如("xpath", "//button[text()='下一页']")）
        :return: 属性值列表（若输入单个文件名，返回长度为1的列表；未找到返回空列表）
        """
        # 支持单个文件名输入（自动转为列表处理）
        if isinstance(filenames, str):
            filenames = [filenames]
        remaining_filenames = filenames.copy()
        attribute_results = []  # 存储所有成功获取的属性值
        supported_strategies = ["id", "xpath", "class name", "accessibility id", "css selector"]  # 支持的定位策略
        
        try:
            # 1. 验证所有定位器策略是否合法
            for locator in [root_layout_locator, file_name_locator, attribute_locator, next_page_locator]:
                if locator is None:
                    continue
                strategy = locator[0].lower()
                if strategy not in supported_strategies:
                    raise ValueError(f"不支持的定位器策略: '{strategy}'，支持的策略：{supported_strategies}")
            
            # 2. 分页查找文件并获取属性
            while remaining_filenames and current_page <= all_pages:
                # 显式等待当前页文件列表加载完成（替代隐式等待，更可靠）
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(root_layout_locator)
                    )
                except TimeoutException:
                    logger.warning(f"第{current_page}页文件列表加载超时，跳过当前页")
                    current_page += 1
                    continue
                
                # 获取当前页所有文件项
                file_items = self.driver.find_elements(*root_layout_locator)
                logger.info(f"第{current_page}页共有{len(file_items)}个文件项")
                
                # 遍历当前页文件项，匹配目标文件名
                for target_filename in list(remaining_filenames):
                    found = False
                    for item in file_items:
                        try:
                            # 查找当前文件项的文件名元素
                            name_element = item.find_element(*file_name_locator)
                            current_filename = name_element.text.strip()
                            
                            if current_filename == target_filename:
                                # 找到目标文件，获取其属性元素的属性值
                                try:
                                    # 显式等待属性元素可见
                                    attr_element = WebDriverWait(item, 5).until(
                                        EC.visibility_of_element_located(attribute_locator)
                                    )
                                    attribute_value = attr_element.get_attribute(attribute)
                                    # 处理文本属性的空白（如" 2025-11-04 09:19:46 " → "2025-11-04 09:19:46"）
                                    if attribute == "text" and attribute_value:
                                        attribute_value = attribute_value.strip()
                                    attribute_results.append(attribute_value)
                                    logger.info(
                                        f"第{current_page}页：成功获取文件[{target_filename}]的属性 → {attribute_value}"
                                    )
                                    remaining_filenames.remove(target_filename)
                                    found = True
                                    break  # 跳出当前文件项循环，继续下一个文件名
                                except (TimeoutException, NoSuchElementException) as attr_e:
                                    logger.error(
                                        f"文件[{target_filename}]的属性元素查找失败：{attr_e}，定位器：{attribute_locator}"
                                    )
                                    # 属性获取失败但文件已找到，不再重复查找
                                    remaining_filenames.remove(target_filename)
                                    found = True
                                    break
                        except NoSuchElementException:
                            logger.debug(f"文件项中未找到文件名元素（定位器：{file_name_locator}），跳过当前项")
                            continue
                        except Exception as e:
                            logger.debug(f"处理第{current_page}页文件项时出错：{e}，继续下一项")
                            continue
                    
                    if not found:
                        logger.debug(f"第{current_page}页未找到文件：{target_filename}")
                
                # 3. 翻页逻辑（若还有未找到的文件）
                if remaining_filenames and next_page_locator:
                    try:
                        # 显式等待下一页按钮可点击
                        next_page_btn = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(next_page_locator)
                        )
                        next_page_btn.click()
                        logger.info(f"翻到第{current_page + 1}页")
                        current_page += 1
                    except (TimeoutException, NoSuchElementException) as e:
                        logger.warning(f"无法翻到第{current_page + 1}页（可能是最后一页）：{e}")
                        break  # 翻页失败，终止循环
                else:
                    break  # 无下一页或已找到所有文件，终止循环
            
            # 4. 记录未找到的文件
            for filename in remaining_filenames:
                logger.warning(f"所有页面（共{all_pages}页）均未找到文件：{filename}")
            
            logger.info(f"总成功获取{len(attribute_results)}/{len(filenames)}个文件的属性")
            return attribute_results
        
        except ValueError as ve:
            # 定位器策略错误（提前暴露配置问题）
            logger.error(f"参数错误：{ve}")
            raise  # 抛出错误，让调用方感知配置问题
        except Exception as e:
            logger.error(f"获取文件属性时发生未知错误：{e}")
            return attribute_results  # 即使出错，也返回已成功获取的结果
    
    def get_locator_checked_status(self, root_layout_locator, file_name_locator, checkbox_locator, attribute,
                                   filenames):
        """
        根据多个文件名获取对应的复选框状态
        :return: 字典格式 {文件名: 选中状态}
        """
        status_dict = {}
        try:
            file_items = self.driver.find_elements(*root_layout_locator)
            logger.info(f"共有{len(file_items)}个文件项")
            
            for target_filename in filenames:
                found = False
                for item in file_items:
                    try:
                        name_element = item.find_element(*file_name_locator)
                        current_filename = name_element.text
                        
                        if current_filename == target_filename:
                            checkbox_element = item.find_element(*checkbox_locator)
                            # 获取选中状态
                            status = checkbox_element.get_attribute(attribute)
                            status_dict[target_filename] = status
                            found = True
                            logger.info(f"文件 {target_filename} 状态: {status}")
                            break
                    except Exception as e:
                        logger.debug(f"处理文件项时出错: {e}")
                        continue
                
                if not found:
                    logger.warning(f"未找到文件: {target_filename}")
                    status_dict[target_filename] = "未找到"
            
            return status_dict
        
        except Exception as e:
            logger.error(f"获取文件状态时发生异常: {e}")
            # 返回默认状态字典
            return {filename: "获取失败" for filename in filenames}
    
    def get_child_elements_text_by_parent(self, parent_locator, child_locator):
        """
        根据父元素定位器，获取所有子元素的text属性，返回文本列表
        :param parent_locator: 父元素定位器
        :param child_locator: 子元素定位器
        :return: 子元素文本列表（如 ['文本1', '文本2']），无数据时返回空列表
        """
        try:
            # 1. 等待父元素出现（可见或存在，根据实际场景选择）
            logger.info(f"等待父元素出现：{parent_locator}")
            parent_element = self.wait_for_element(parent_locator)
            
            # 2. 在父元素范围内查找所有子元素
            logger.info(f"在父元素 {parent_locator} 下查找子元素：{child_locator}")
            child_elements = parent_element.find_elements(*child_locator)  # * 解包定位器元组
            
            if not child_elements:
                logger.warning(f"父元素 {parent_locator} 下未找到任何子元素 {child_locator}")
                return []
            
            # 3. 遍历子元素，获取text属性
            child_texts = []
            for index, element in enumerate(child_elements, 1):
                text = element.text  # 去除首尾空格
                child_texts.append(text)
                self.logger.debug(f"第 {index} 个子元素文本：{text}")
            
            logger.info(f"成功获取 {len(child_texts)} 个子元素文本")
            return child_texts
        
        except TimeoutException:
            logger.error(f"父元素 {parent_locator} 定位超时（{self.timeout}s）")
            return []
        except NoSuchElementException:
            logger.error(f"父元素 {parent_locator} 存在，但未找到子元素 {child_locator}")
            return []
        except Exception as e:
            logger.error(f"获取子元素文本失败：{str(e)}", exc_info=True)
            return []
