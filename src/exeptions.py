class ApolloError(Exception):
    def __init__(self, *bad_params):
        self.bad_params = bad_params

    def get_messages(self):
        return [self.template.format(name) for name in self.bad_params]


class NotIntError(ApolloError):
    template = 'Значение параметра "{}" не целое число!'


class SmallConsoleError(ApolloError):
    template = 'Место для отката {}мм не достаточно!'


class FileNotExistError(ApolloError):
    template = 'Файл {} не найден!'

class SketchNotFoundByConditionError(ApolloError):
    template = 'Нет чертежа {} соответствующего введенным данным'