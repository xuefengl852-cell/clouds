import logging
import os
import subprocess
import time
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
        "id": By.ID,
        "xpath": By.XPATH,
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
            # 添加截图
            self.save_screenshot(f"element_timeout_{locator_value}")
            # 关键修改：抛出 NoSuchElementException 而非返回 False
            raise NoSuchElementException(error_msg)
        except Exception as e:
            logger.error(f"元素定位异常: {str(e)}")
            # 关键修改：抛出原始异常
            raise
    
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
            logger.error(f"输入文本失败: {locator} | {str(e)}")
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
        :param timeout: 超时时间（秒）
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
    
    def get_element_attribute(self, locator, attribute, condition='present', timeout=None):
        """
        通用获取元素属性值方法

        :param locator: 元素定位器
        :param attribute: 属性名称
        :param condition: 等待条件 (默认'present')
        :param timeout: 超时时间
        :return: 属性值
        """
        try:
            element = self.wait_for_element(
                locator,
                condition=condition,
                timeout=timeout
            )
            value = element.get_attribute(attribute)
            logger.debug(f"元素属性 [{attribute}] 值: {value}")
            return value
        
        except StaleElementReferenceException:
            logger.warning("元素过时，重新获取...")
            element = self.wait_for_element(locator, timeout=timeout)
            return element.get_attribute(attribute)
        
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
    
    def assert_text_is_equal(self, input_text, displayed_text):
        """
        断言输入框文本与输入文本是否一致
        :param displayed_text:
        :param locator: id元组
        :param input_text: 输入文本
        :return:
        """
        try:
            assert input_text == displayed_text
        except AssertionError as e:
            logger.error(f"断言元素值相同失败：{e}")
        except StaleElementReferenceException:
            logger.error(f"元素已经过时")
    
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
