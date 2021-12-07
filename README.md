# monitorGunplaReleaseInfo.py


```
usage: monitorGunplaReleaseInfo.py [-h] [-f FILE] [-c [CATEGORY ...]] [-n] [-w] [-a AFTER] [-m]

[Options] Detailed options -h or --help

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  load stored Bandai's PDF file.
  -c [CATEGORY ...], --category [CATEGORY ...]
                        check specific category. e.g. MG, RG
  -n, --new             check only NEW products
  -w, --wishlist        filter by wish_list.csv
  -a AFTER, --after AFTER
                        filter by date. e.g. 20211215 for 2021/12/15
  -m, --moniter         monitor upcoming sales products
```
  
  
 Format of Wish List(csv file)
 <productID>,<amount of purchase>

Sample
```
5057525,2
5062932,1
5063094,3
5063157,1
5063191,1
 
```


Sample output


```
python monitorGunplaReleaseInfo.py -m -c  旧キット -a 20211222
<< 発売日:2021-12-23(木) >>
商品ID:5063153, 商品名:1/100 シャア専用ザク, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063154, 商品名:1/100 量産ザク, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063159, 商品名:1/550 ブラウブロ, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063162, 商品名:1/100 グフ, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063164, 商品名:1/100 シャアゲルググ, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063165, 商品名:1/100 量産ゲルググ, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063168, 商品名:1/100 ゴック, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063169, 商品名:1/100 アッグガイ, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063171, 商品名:1/144 Gアーマー, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063173, 商品名:1/60 ガンダム, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063176, 商品名:1/60 シャアゲルググ, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063177, 商品名:1/60 量産ゲルググ, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063178, 商品名:1/60 ドム, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063179, 商品名:1/72 メカガンダム, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063180, 商品名:1/72 メカニックザク, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063181, 商品名:1/100 リアルガンダム, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063186, 商品名:1/100 リアルドム, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063187, 商品名:1/100 リアルゲルググ, 商品カテゴリー:旧キット, 購入予定:0個
Price(only WishList): 0
Price when buying one by one : 23900

<< 発売日:2021-12-27(月) >>
商品ID:5063155, 商品名:1/100 ガンキャノン, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063156, 商品名:1/100 ギャン, 商品カテゴリー:旧キット, 購入予定:0個
*商品ID:5063157, 商品名:1/100 旧型ザク, 商品カテゴリー:旧キット, 購入予定:1個
商品ID:5063158, 商品名:1/100 ジム, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063161, 商品名:1/100 アッガイ, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063182, 商品名:1/100 リアルザク, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063183, 商品名:1/100 リアルガンキャノン, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063184, 商品名:1/100 リアル旧ザク, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063185, 商品名:1/100 リアルジム, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063188, 商品名:1/250 ランバラル特攻, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063189, 商品名:1/250  ジャブローに散る, 商品カテゴリー:旧キット, 購入予定:0個
商品ID:5063190, 商品名:1/250  テキサスの攻防, 商品カテゴリー:旧キット, 購入予定:0個
*商品ID:5063191, 商品名:1/250  ア・バオア・クー, 商品カテゴリー:旧キット, 購入予定:1個
Price(only WishList): 1400
Price when buying one by one : 9100

Total price(only WishList): 1400
Total price when buying one by one : 33000



```
