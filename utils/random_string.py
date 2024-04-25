#8-5 スラッグフィールドのデフォルト値を関数で設定する方法
#8-5 generator 反復装置生成装置
#char 文字列
import random,string

def random_string_generator(size=20, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


'''
#まずは、ランダムに選ぶ文字の候補を定義します。Pythonでは「stringモジュール」を使うと便利です！a~zは「ascii_lowercase」、A～Zは「ascii_uppercase」、数字は「digits」で取得することができます！
## 結合演算子「+」を使う
first = 'shinji'
last = 'kawasaki'
name = first + ' ' + last  # 文字列変数とリテラル文字列と文字列変数の結合
print(name)  # 'shinji kawasaki'

# 累算代入演算子「+=」を使う
name = 'shinji'
name += ' ' + 'kawasaki'
print(name)  # 'shinji kawasaki'

# 文字列のjoinメソッドを使う
somestr = 'one, two, three'
strlist = somestr.split(', ')
print(strlist)  # ['one', 'two', 'three']
result = '_'.join(strlist)  # 区切りを'_'として['one', 'two', 'three']を結合
print(result)  # one_two_three

# 区切り文字が必要なければ空文字列に対してjoinメソッドを呼び出す
result = ''.join(strlist)
print(result)  # onetwothree

# 数値を要素とするリストから、それらを文字列化して結合
nums = list(range(5))  # [0, 1, 2, 3, 4]
result = ', '.join([str(x) for x in nums])
print(result)  # '0, 1, 2, 3, 4'
'''