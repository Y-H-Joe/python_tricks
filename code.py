###报出详细错误信息
###但是输出是黑白的
import traceback

def func(file,*args,**kwargs):
    try:
        pass
    except Exception as e:
        '''
        #这个是输出错误类别的，如果捕捉的是通用错误
        #输出  str(Exception):	<type 'exceptions.Exception'>
        print('str(Exception):\t', str(Exception))
        #这个是输出错误的具体原因，这步可以不用加str，输出
        #输出 str(e):		integer division or modulo by zero
        print('str(e):\t\t', str(e))
        #输出 repr(e):	ZeroDivisionError('integer division or modulo by zero',)
        print('repr(e):\t', repr(e))
        #以下两步都是输出错误的具体位置的
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        '''
        traceback.print_exc()
