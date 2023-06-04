"""
关于单例实现
"""

"""
通过定义方式使得类为单例
class MyClass(object, metaclass=SingletonMetaClass):
"""
class SingletonMetaClass(type):
    def __call__(self, *args, **kwargs):
        """
        self : class Singleton
        """
        if not hasattr(self, "ins"):
            insObject = super(__class__, self).__call__(*args, **kwargs)
            setattr(self, "ins", insObject)
        return getattr(self, "ins")


"""
通过注释方法使得类为单例
@Singleton
class MySQLHelper(object):    
"""
def Singleton(clsObject):
    def inner(*args, **kwargs):
        if not hasattr(clsObject, "ins"):
            insObject = clsObject(*args, **kwargs)
            setattr(clsObject, "ins", insObject)
        return getattr(clsObject, "ins")
    return inner

"""
通过集成的方式使得类为单例
class MySQLHelper(SingletonClass):
"""
class SingletonClass:
    def __new__(cls, *args, **kwargs) -> object:
        """
        cls : class Singeton
        """
        if not hasattr(cls, "ins"):
            insObject = super(__class__, cls).__new__(cls, *args, **kwargs)
            setattr(cls, "ins", insObject)
        return getattr(cls, "ins")