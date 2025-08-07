import pandas as pd
from collections import Counter

def calculate_daily_food_percentages(input_csv, output_csv):
    df = pd.read_csv(input_csv, encoding="utf-8-sig")
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.date

    food_keywords = [
        'طحين', 'سكر', 'زيت', 'رز', 'خبز', 'خميرة','دقيق', 'ملح', 'عدس', 'فول', 'حمص', 'تمر', 'فستق', 'لبن', 'جبنة', 'بيض', 'شاي', 'قهوة', 'معكرونة', 'مكرونة', 'عسل', 'سمك', 'لحم', 'دجاج','برغل','صلصة','حلاوة','السيرج','سيرج','الطحين', 'السكر', 'الزيت', 'الرز', 'الخبز', 'الخميرة', 'الدقيق', 'الملح', 'العدس', 'الفول', 'الحمص', 'التمر', 'الفستق', 'اللبن', 'الجبنة', 'البيض', 'الشاي', 'القهوة', 'المعكرونة', 'المكرونة', 'العسل', 'السمك', 'اللحم', 'الدجاج',
        # Vegetables
        'بطاطا', 'بطاطس', 'بندورة', 'طماطم', 'خيار', 'فلفل', 'باذنجان', 'كوسا', 'جزر', 'بصل', 'ثوم', 'ملفوف', 'زهرة', 'فاصوليا', 'بازيلاء', 'سبانخ', 'خس', 'جرجير', 'فجل', 'قرع', 'فطر', 'ورق عنب', 'فول اخضر', 'فول أخضر', 'شمندر', 'كرفس', 'نعنع', 'بقدونس', 'كزبرة', 'شبت',
        # Fruits
        'تفاح', 'موز', 'برتقال', 'ليمون', 'عنب', 'رمان', 'خوخ', 'مشمش', 'دراق', 'كمثرى', 'اجاص', 'تين', 'بطيخ', 'شمام', 'فراولة', 'كيوي', 'مانجو', 'مانغا', 'جوافة', 'اناناس', 'بابايا', 'رمان', 'كرز', 'توت', 'تمر هندي', 'قشطة', 'جريب فروت', 'يوسفي', 'نكتارين', 'برقوق', 'جوز الهند'
    ]
    results = []
    for day, group in df.groupby('day'):
        text = " ".join(group['text'].dropna())
        words = text.split()
        food_words = [w for w in words if w in food_keywords]
        total_food_words = len(food_words)

        if total_food_words == 0:
            continue
        word_freq = Counter(food_words)
        daily_data = {'day': day}

        for food in food_keywords:
            daily_data[food] = round((word_freq[food] / total_food_words) * 100, 2) if food in word_freq else 0.0

        results.append(daily_data)

    daily_df = pd.DataFrame(results)
    daily_df.to_csv(output_csv, index=False, encoding="utf-8-sig")
