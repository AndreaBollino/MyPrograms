import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('alogger')
logger.debug("Debug message")
#logger = logging.getLogger('alogger')
#logger.debug("Debug message")

#logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(filename='logs.log', level=logging.DEBUG)
#logging.basicConfig(filename='logs.log', level=logging.DEBUG,
 #                   format='%(asctime)s-%(levelname)s:%(funcName)s:%(message)s')

def foo(x:int, y:int) -> int:
    return x*y
def boo(a: str, b: str) -> str:
    return f"hai pssato {a} and {b} "

val_foo = foo(3, 4)
val_boo = boo("Hello","World")

logging.debug(f"Your values are: foo: {val_foo} and boo: {val_boo}")
logging.warning(f"Your values are: foo: {val_foo} and boo: {val_boo}")
#####OUT
#WARNING:root:Your values are: foo: 12 and boo: You have passed Hello and World