import csv
import random
import time

print('ファイル読み込み中...')
#応募状況を把握
with open('test.csv',newline='',encoding='utf8') as csv_file:
  f = csv.reader(csv_file)
  comment = next(f)
  #header = next(f)ヘッダー用
  grANDcllist1 = []
  grANDcllist2 = []

  print(comment)

  for row in f:
    grades = str(row[0])
    classes = str(row[1])
    numbers = str(row[2])
    classesapp1 = str(row[3])
    classesapp2 = str(row[4])

    grANDcl = grades + classes + numbers#生徒の情報
    grANDcllist1.append(grANDcl)
    grANDcllist1.append(classesapp1)#生徒の情報、第一希望・・・のリスト
    grANDcllist2.append(grANDcl)
    grANDcllist2.append(classesapp2)#生徒の情報、第二希望・・・のリスト

  limit = len(grANDcllist1)
  i=0
  stuappperclas1={}#クラス,生徒のリストの辞書
  gradeandclasses=['5A','5B','5C','5D','6A','6B','6C','6D']
  #クラスごとに辞書を作って格納
  while i+2<=limit:
    for cl in gradeandclasses:
      if(grANDcllist1[i+1] == cl):
        try:
          if type(stuappperclas1[cl]) == str:
            #getstuapperclas = str(stuappperclas1[cl])
            getstuapperclas = [str(stuappperclas1[cl]),str(grANDcllist1[i])]
            stuappperclas1[cl] = getstuapperclas
          else:
            getstuapperclas = list(stuappperclas1[cl])#現在のclに対応している生徒のリストを取得
            getstuapperclas.append(grANDcllist1[i])
            stuappperclas1[cl]=getstuapperclas
        except KeyError:
          stuappperclas1[cl] = str(grANDcllist1[i])#未登録のmapだった時clとそれに対応する生徒のリストを代入1回目だけ動くかな
        break
    i+=2
  limit = len(grANDcllist2)
  i=0
  stuappperclas2={}
  while i+2<=limit:
    for cl in gradeandclasses:
      if(grANDcllist2[i+1] == cl):
        try:
          if type(stuappperclas2[cl]) == str:
            #getstuapperclas = str(stuappperclas1[cl])
            getstuapperclas = [str(stuappperclas2[cl]),str(grANDcllist2[i])]
            stuappperclas2[cl] = getstuapperclas
          else:
            getstuapperclas = list(stuappperclas2[cl])#現在のclに対応している生徒のリストを取得
            getstuapperclas.append(grANDcllist2[i])
            stuappperclas2[cl]=getstuapperclas
        except KeyError:
          stuappperclas2[cl] = str(grANDcllist2[i])#未登録のmapだった時clとそれに対応する生徒のリストを代入1回目だけ動くかな
        break
    i+=2
print('ファイルの読み込みを完了しました')

#データの整理
entrantamount ={}
entrantamount['5A'] = len(stuappperclas1['5A'])
entrantamount['5B'] = len(stuappperclas1['5B'])
entrantamount['5C'] = len(stuappperclas1['5C'])
entrantamount['5D'] = len(stuappperclas1['5D'])
entrantamount['6A'] = len(stuappperclas1['6A'])
entrantamount['6B'] = len(stuappperclas1['6B'])
entrantamount['6C'] = len(stuappperclas1['6C'])
entrantamount['6D'] = len(stuappperclas1['6D'])
#大きい順にクラスを並べる マルチスレッド用に作ったんだけど逆に重くなりそう
i = 0
n = 0
sortedentrantclass=[]#大きい順に並んだクラスが入る
while n < 8:
  for cl in entrantamount:
    if entrantamount[cl] >= i:
      bigcl = str(cl)
      i = entrantamount[cl]
  sortedentrantclass.append(bigcl)
  del entrantamount[bigcl]
  i=0
  n+=1


#一回目の抽選(当選経験者の補正無し)
def FirstLottery():
  winnerstudent = []
  winnerstudentmap = {}
  i=0
  for cl in sortedentrantclass:
    if len(stuappperclas1[cl]) > 40:
      while i < 40:
        choicedstudent = random.choice(stuappperclas1[cl])
        winnerstudent.append(choicedstudent)
        delete = stuappperclas1[cl].index(choicedstudent)
        del stuappperclas1[cl][delete]
        i+=1
    else:
      winnerstudent = stuappperclas1[cl]
    winnerstudentmap[cl] = winnerstudent
    winnerstudent = []
    i=0
  return winnerstudentmap


#30人だけ
def FirstLotteryForDebag():
  winnerstudent = []
  winnerstudentmap = {}
  i=0
  for cl in sortedentrantclass:
    if len(stuappperclas1[cl]) > 30:
      while i < 30:
        choicedstudent = random.choice(stuappperclas1[cl])
        winnerstudent.append(choicedstudent)
        delete = stuappperclas1[cl].index(choicedstudent)
        del stuappperclas1[cl][delete]
        i+=1
    else:
      winnerstudent = stuappperclas1[cl]
    winnerstudentmap[cl] = winnerstudent
    winnerstudent = []
    i=0
  return winnerstudentmap


#当選者を探して下方修正 入れるのは第二希望のリスト(クラス別で出したもの)、一回目の抽選の当選者全員のマップ(値がリストになってるやつ)、抽選のクラスだけで 第一希望で当選した人、当選してなかった人を選んでlistでﾘﾀｰﾝする
def DecideDownwardRevision(secondplayerslist,winnerstudentmap,classname):
  returnFirstWinner=[]
  for classes in gradeandclasses:
    for winnerstudent in winnerstudentmap[classes]:#すべての当選者がwinnerstudentに入る
      try:
        delete = secondplayerslist.index(winnerstudent)
        del secondplayerslist[delete]
        returnFirstWinner.append(winnerstudent)
      except ValueError:
        pass
  return [returnFirstWinner,secondplayerslist]




def SecondLottery(times,winnerlist,notwinnerlist):#抽選の回数、当選経験者のリスト、当選未経験者のリストが入り、2回目の抽選で当選した人がリストでﾘﾀｰﾝされる
  ForLottery = [] #一回も当選したことない人が100倍に増えて入って、一回当選された人が100-n倍に増えて入るところ
  n = 30
  trialamout = 0
  i = 0
  for insert in notwinnerlist:
    while i < 100:
      ForLottery.append(insert)
      i+=1
    i=0
  for insert in winnerlist:
    while i < 100-n:
      ForLottery.append(insert)
      i+=1
    i=0
  choiceresult = []
  while trialamout < times:
    random.seed()
    result = random.choice(ForLottery)
    trialamout+=1
    choiceresult.append(result)
    if result in winnerlist:
      deletetime = 100-n
    else:
      deletetime = 100
    m = 0
    while m < deletetime:
      ForLottery.remove(result)
      m+=1
  return choiceresult

  
#CUI部分
print('実行したい処理の番号を入力してください')
command = int(input('デバッグ(30人だけ一次抽選し、10人だけ二次抽選):1 \n普通に抽選:2 \nキャンセル処理\n数字を入れてEnterを押してください:'))
start = time.time()
LotteryMap={}
if command == 1:
  winnermap = FirstLotteryForDebag()
  for cls in gradeandclasses:
    listtest = DecideDownwardRevision(stuappperclas2[cls],winnermap,cls)
    times = 40 - len(winnermap[cls])
    LotteryMap[cls]= SecondLottery(int(times),list(listtest[0]),list(listtest[1]))
    LotteryMap[cls].extend(winnermap[cls])
if command == 2:
  winnermap = FirstLottery()
  for cls in gradeandclasses:
    if len(winnermap[cls]) == 40:
      pass
    else:
      listtest = DecideDownwardRevision(stuappperclas2[cls],winnermap,cls)
      times = 40 - len(winnermap[cls])
      LotteryMap[cls]=SecondLottery(int(times),list(listtest[0]),list(listtest[1]))


#当選者のリストをファイルに入れます
with open('lottely.csv', 'w', newline="") as f:#当選者のリストを作成(csv)
  writer = csv.writer(f)
  for cl in gradeandclasses:
    writer.writerow(list(cl))
    for student in LotteryMap[cl]:
      grade = student[0]
      classes = student[1]
      number = student[2:]
      writer.writerow([grade,classes,number])
  f.close()
elapsed_time = time.time() - start
thmap = {'1':'16','2':'15','3':'14','4':'13','5':'12','6':'11'}
with open('copipe.txt', 'w', newline="", encoding="utf-8") as f:#当選者のリストを作成(txt)
  for cl in gradeandclasses:
    f.write(cl[0]+"年"+cl[1]+"組の劇の当選者:\n")
    for student in sorted(LotteryMap[cl]):
      f.write(str(student[0])+"年"+str(student[1])+"組"+student[2:]+"番@"+str(student)+"KSS"+thmap[student[0]]+"\n")
print('処理時間:'+str(elapsed_time))
print('抽選後のファイルを作成しました')