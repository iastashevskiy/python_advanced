
# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и 
# проверить тип и содержание соответствующих переменных. 

def encode(word):
	return word.encode('utf-8')


first = encode('разработка')
second = encode('сокет')
third = encode('декоратор')
print(first,'\n', second,'\n', third)

# Каждое из слов «class», «function», «method» записать в байтовом типе без 
# преобразования в последовательность кодов (не используя методы encode и decode) и
# определить тип, содержимое и длину соответствующих переменных.

first = b'class'
second = b'function'
third = b'method'
print(first,'\n', second,'\n', third)

# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно 
# записать в байтовом типе.

# ОТВЕТ:
# Все можно представить в байтовом типе, только слова "класс" и "функция" необходимо
#  переводить методом encode('utf-8'), так как эти символы не входят в ASCII


# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из 
# строкового представления в байтовое и выполнить обратное преобразование 
# (используя методы encode и decode).

def decode(expression):
	return expression.decode('utf-8')

first = encode('разработка')
second = encode('администрирование')
third = encode('protocol')
fourth = encode('standard')
print(first,'\n', second,'\n', third, "\n", fourth)


first = decode(first)
second = decode(second)
third = decode(third)
fourth = decode(fourth)
print(first,'\n', second,'\n', third, "\n", fourth)