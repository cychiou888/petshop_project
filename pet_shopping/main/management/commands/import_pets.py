from django.core.management.base import BaseCommand
from main.models import Pet

class Command(BaseCommand):
    help = '從 pet_shop.js 導入寵物資料到資料庫'

    def handle(self, *args, **options):
        # 首先清空現有的寵物資料（可選）
        Pet.objects.all().delete()
        
        # 寵物資料，從 pet_shop.js 轉換而來
        pets_data = [
            {
                "name": "柴犬",
                "breed": "日本柴犬",
                "price": "NT$45,000",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "3個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/87c2f14e-shiba_29.jpg",
                "category": "dogs",
                "description": "柴犬是日本國寶級犬種，以其忠誠和機靈著稱。臉上標誌性的「柴笑」讓人愛不釋手。性格活潑、警覺性高，適合居家飼養。本犬舍柴犬均來自純種血統，身體健康，社會化訓練良好。"
            },
            {
                "name": "邊境牧羊犬",
                "breed": "邊境牧羊犬",
                "price": "NT$52,000",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "2個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/a596034d-border_collie_79.jpg",
                "category": "dogs",
                "description": "邊境牧羊犬被譽為「狗中博士」，智商在所有犬種中名列前茅。非常適合做運動夥伴，精力充沛，需要大量運動和智力訓練。個性溫和友善，但需要耐心訓練和足夠的活動空間。"
            },
            {
                "name": "法國鬥牛犬",
                "breed": "法國鬥牛犬",
                "price": "NT$68,000",
                "status": "即將到貨",
                "statusClass": "status-coming",
                "age": "3個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/fb227026-French_Bulldog_48.jpg",
                "category": "dogs",
                "description": "法鬥以其獨特的蝙蝠耳和討喜的性格聞名。體型小巧，適合公寓飼養。性格活潑開朗，親人愛玩，是理想的居家寵物。本店法鬥來自專業繁育，品相優良，保證健康。"
            },
            {
                "name": "貴賓犬",
                "breed": "迷你貴賓犬",
                "price": "NT$35,000",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "2.5個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/guest_dog.jpg",
                "category": "dogs",
                "description": "貴賓犬優雅聰明，幾乎不掉毛，是過敏體質者的理想選擇。性格活潑，容易訓練，非常適合家庭飼養。定期美容可以讓牠保持漂亮的外表，是既可愛又好照顧的絕佳選擇。"
            },
            {
                "name": "拉布拉多",
                "breed": "拉布拉多尋回犬",
                "price": "NT$42,000",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "2個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/raburado.jpg",
                "category": "dogs",
                "description": "拉布拉多是最受歡迎的大型犬之一，性格溫和友善，特別適合有孩子的家庭。智商高，容易訓練，常被培訓為導盲犬或搜救犬。本犬舍拉布拉多品種純正，遺傳疾病檢測皆為陰性。"
            },
            {
                "name": "英國短毛貓",
                "breed": "英國短毛貓",
                "price": "NT$38,000",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "3個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/cat_1.webp",
                "category": "cats",
                "description": "英短貓以其圓潤的身材和可愛的外表聞名，被譽為「泰迪熊貓咪」。性格溫和穩重，適合初次養貓的家庭。毛色為藍灰色，被毛短密，好打理，是理想的室內寵物。"
            },
            {
                "name": "波斯貓",
                "breed": "波斯貓",
                "price": "NT$45,000",
                "status": "即將到貨",
                "statusClass": "status-coming",
                "age": "3個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/cat_2.jpg",
                "category": "cats",
                "description": "波斯貓是最古老的貓種之一，以其優雅的長毛和平和的性格著稱。面部扁平，眼大圓潤，是高貴優雅的代表。雖然需要定期梳理毛髮，但溫馴的性格和美麗的外表使其深受歡迎。"
            },
            {
                "name": "緬因貓",
                "breed": "緬因庫恩貓",
                "price": "NT$55,000",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "3個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/cat_3.jpeg",
                "category": "cats",
                "description": "緬因貓是最大的家貓品種之一，被稱為「溫柔的巨人」。性格友善，喜歡和主人互動，忠誠度高。半長毛易於打理，適合家庭飼養。本貓舍緬因貓均為純種，骨架大，毛質好。"
            },
            {
                "name": "蘇格蘭摺耳貓",
                "breed": "蘇格蘭摺耳貓",
                "price": "NT$48,000",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "3個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/cat_4.jpg",
                "category": "cats",
                "description": "蘇格蘭摺耳貓以其獨特的向前摺疊的耳朵而聞名，外表非常可愛。性格溫順，喜歡和主人親近，是理想的伴侶貓。本店摺耳貓基因檢測齊全，確保健康。"
            },
            {
                "name": "暹羅貓",
                "breed": "暹羅貓",
                "price": "NT$42,000",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "3個月",
                "gender": "公/母可選",
                "vaccine": "已完成基礎疫苗",
                "image": "/static/images/cat_5.jpg",
                "category": "cats",
                "description": "暹羅貓是最古老的東方貓種之一，以其藍眼睛和獨特的四肢深色點狀花紋著稱。性格活潑好動，非常黏人，喜歡與主人互動。叫聲特別，智商高，容易訓練。"
            },
            {
                "name": "倉鼠",
                "breed": "布丁倉鼠",
                "price": "NT$200",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "1個月",
                "gender": "公/母可選",
                "vaccine": "已健康檢查",
                "image": "/static/images/ham_1.jpg",
                "category": "small",
                "description": "布丁倉鼠體型小巧，毛色呈金黃色，非常可愛。性格溫順，適合新手飼養。雖然是夜行動物，但經過訓練也可以適應主人的作息。飼養空間需求小，是學生和上班族的理想選擇。"
            },
            {
                "name": "龍貓",
                "breed": "花枝鼠",
                "price": "NT$2,500",
                "status": "可預購",
                "statusClass": "status-available",
                "age": "2個月",
                "gender": "公/母可選",
                "vaccine": "已健康檢查",
                "image": "/static/images/dragon_cat.jpg",
                "category": "small",
                "description": "龍貓是較大型的鼠類寵物，性格溫和，不咬人，容易親近人類。適合家庭飼養，可以和主人建立深厚的感情。需要較大的活動空間和豐富的玩具，壽命比一般倉鼠長。"
            }
        ]
        
        # 將資料導入到資料庫
        for pet_data in pets_data:
    # 刪除不需要的欄位
            if 'age' in pet_data:
                del pet_data['age']
            if 'gender' in pet_data:
                del pet_data['gender']
        Pet.objects.create(**pet_data)
        
        
        
        # 顯示成功訊息
        self.stdout.write(self.style.SUCCESS(f'成功導入 {len(pets_data)} 筆寵物資料'))