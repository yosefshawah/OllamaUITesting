"""Device configuration for responsive testing"""

class DeviceConfig:
    """Configuration for different device types"""
    
    MOBILE = {
        'name': 'mobile',
        'width': 375,
        'height': 812,
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
        'is_mobile': True
    }
    
    TABLET = {
        'name': 'tablet',
        'width': 768,
        'height': 1024,
        'user_agent': 'Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
        'is_mobile': True
    }
    
    DESKTOP = {
        'name': 'desktop',
        'width': 1920,
        'height': 1080,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'is_mobile': False
    }
    
    DESKTOP_SMALL = {
        'name': 'desktop_small',
        'width': 1366,
        'height': 768,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'is_mobile': False
    }
    
    @classmethod
    def get_device_config(cls, device_name):
        """Get device configuration by name"""
        configs = {
            'mobile': cls.MOBILE,
            'tablet': cls.TABLET,
            'desktop': cls.DESKTOP,
            'desktop_small': cls.DESKTOP_SMALL
        }
        return configs.get(device_name.lower(), cls.DESKTOP)
    
    @classmethod
    def is_mobile_device(cls, device_config):
        """Check if device is mobile"""
        return device_config.get('is_mobile', False)
    
    @classmethod
    def get_breakpoint(cls, width):
        """Get breakpoint category based on width"""
        if width < 768:
            return 'mobile'
        elif width < 1024:
            return 'tablet'
        else:
            return 'desktop'
