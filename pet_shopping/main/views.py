from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import time
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Pet
import torch
from pathlib import Path

# 全局變量存儲 YOLO 模型
yolo_model = None

def load_model():
    """載入 YOLOv8 模型"""
    import os
    from pathlib import Path
    
    # 獲取當前文件的絕對路徑
    current_file = Path(__file__).resolve()
    
    # 從當前文件獲取 Django 應用目錄 (main)
    app_dir = current_file.parent
    
    # 獲取 Django 專案目錄 (pet_shopping)
    django_dir = app_dir.parent
    
    # 獲取專案根目錄 (pet_shop)
    project_root = django_dir.parent
    
    # 構建模型文件路徑
    model_path = project_root / 'yolo_model' / 'best.pt'
    
    print(f"嘗試載入模型: {model_path}")
    print(f"模型文件存在: {model_path.exists()}")
    
    # 檢查文件是否存在
    if not model_path.exists():
        raise FileNotFoundError(f"找不到模型文件: {model_path}")
    
    # 載入 YOLOv8 模型
    try:
        # 使用 ultralytics 庫加載 YOLOv8 模型
        from ultralytics import YOLO
        model = YOLO(str(model_path))
        print(f"模型已成功載入，類型: {type(model)}")
        return model
    except Exception as e:
        import traceback
        print(f"模型載入失敗: {str(e)}")
        print(traceback.format_exc())
        return None
def pet_detection(request):
    """寵物辨識頁面"""
    return render(request, 'main/pet_detection.html')

@csrf_exempt
def detect_pet(request):
    """處理上傳的圖片並進行寵物辨識"""
    global yolo_model
    
    if request.method != 'POST' or 'image' not in request.FILES:
        return JsonResponse({'success': False, 'message': '請上傳圖片'})
    
    try:
        # 調試信息
        import os
        from pathlib import Path
        
        current_file = Path(__file__).resolve()
        app_dir = current_file.parent
        django_dir = app_dir.parent
        project_root = django_dir.parent
        
        print(f"當前文件: {current_file}")
        print(f"應用目錄: {app_dir}")
        print(f"Django目錄: {django_dir}")
        print(f"專案根目錄: {project_root}")
        print(f"當前工作目錄: {os.getcwd()}")
        
        # 第一次使用時載入模型
        if yolo_model is None:
            yolo_model = load_model()
            if yolo_model is None:
                return JsonResponse({
                    'success': False,
                    'message': '模型載入失敗'
                })
        
        # 獲取上傳的圖片
        image = request.FILES['image']
        
        # 儲存上傳的圖片到臨時文件
        import uuid
        temp_filename = f"{uuid.uuid4()}_{image.name}"
        
        # 使用 project_root 直接定義臨時文件路徑
        temp_dir = project_root / 'media' / 'temp'
        temp_path = temp_dir / temp_filename
        
        # 確保目錄存在
        os.makedirs(temp_dir, exist_ok=True)
        
        print(f"臨時文件目錄: {temp_dir}")
        print(f"臨時文件路徑: {temp_path}")
        
        # 寫入文件
        with open(temp_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # 使用 YOLOv8 模型進行辨識
        results = yolo_model(str(temp_path))
        
        # 處理 YOLOv8 辨識結果
        if len(results) == 0 or len(results[0].boxes) == 0:
            return JsonResponse({
                'success': False,
                'message': '沒有檢測到任何寵物'
            })
        
        # 獲取最可能的寵物類別
        boxes = results[0].boxes
        confidences = boxes.conf.cpu().numpy()  # 獲取所有置信度
        best_idx = confidences.argmax()  # 獲取最高置信度的索引
        
        # 獲取類別 ID 和置信度
        class_id = int(boxes.cls[best_idx].item())
        confidence = float(confidences[best_idx])
        
        # 獲取類別名稱
        detected_class = results[0].names[class_id]
        
        print(f"檢測結果: {detected_class}, 可信度: {confidence}")
        
        # 根據檢測到的類別獲取對應類別的寵物
        pet_mapping = {
            'dog': 'dogs',
            'cat': 'cats',
            'hamster': 'small',
            # 根據你的 YOLO 模型添加更多映射
        }
        
        # 根據檢測到的類別獲取對應的寵物類別
        category = pet_mapping.get(detected_class.lower(), 'dogs')  # 默認為狗
        
        # 從數據庫獲取相似寵物
        from .models import Pet
        similar_pets = list(Pet.objects.filter(category=category).values())
        
        # 返回檢測結果和相似寵物
        return JsonResponse({
            'success': True,
            'detected_class': detected_class,
            'confidence': confidence,
            'image_url': f"/media/temp/{temp_filename}",
            'similar_pets': similar_pets
        })
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': f'處理圖片時出錯: {str(e)}'
        })

def test_paths(request):
    """測試路徑設置是否正確"""
    import os
    from pathlib import Path
    
    current_file = Path(__file__).resolve()
    app_dir = current_file.parent
    django_dir = app_dir.parent
    project_root = django_dir.parent
    model_path = project_root / 'yolo_model' / 'best.pt'
    temp_dir = project_root / 'media' / 'temp'
    
    # 確保臨時目錄存在
    os.makedirs(temp_dir, exist_ok=True)
    
    paths_info = {
        'Django應用目錄': str(app_dir),
        'Django專案目錄': str(django_dir),
        '專案根目錄': str(project_root),
        'YOLO模型路徑': str(model_path),
        '臨時文件目錄': str(temp_dir)
    }
    
    existence = {key: os.path.exists(path) for key, path in paths_info.items()}
    
    return JsonResponse({
        '路徑信息': paths_info,
        '路徑存在': existence
    })

def index(request):
    # 檢查是否登入
    user_id = request.session.get('user_id')
    full_name = request.session.get('full_name')
    
    context = {
        'is_logged_in': user_id is not None,
        'full_name': full_name
    }
    return render(request, 'main/index.html', context)

def pet_shop(request):
    return render(request, 'main/pet_shop.html')

def picture_analyzer(request):
    return render(request, 'main/picture_analyzer.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                # 登入成功，儲存用戶資訊到 session
                request.session['user_id'] = user.id
                request.session['full_name'] = f"{user.first_name} {user.last_name}"
                return redirect('index')
        except User.DoesNotExist:
            return render(request, 'main/login.html', {'error': '登入失敗'})
            
    return render(request, 'main/login.html')

def logout_view(request):
    # 清除 session
    request.session.flush()
    return redirect('log')

def login(request):
    return render(request, 'main/login.html')

def about_us(request):
    return render(request, "main/about_us.html")

def header(request):
    return render(request, "main/header.html")

def footer(request):
    return render(request, "main/footer.html")

def contact_us(request):
    return render(request, "main/contact_us.html")

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('fName')
        last_name = request.POST.get('LName')
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 檢查email是否已存在
        if User.objects.filter(email=email).exists():
            return render(request, 'main/login.html', {'error': '此email已被註冊'})
            
        # 創建新用戶
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password)  # 加密密碼
        )
        
        # 自動登入新用戶
        request.session['user_id'] = user.id
        return redirect('index')  # 導向首頁
        
    return render(request, 'main/login.html')