# 0G Storage Scan Bot

![Banner](https://img.shields.io/badge/0G%20Storage-Scan%20Bot-blue?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**0G Storage Scan Bot** is an automated tool designed to interact with the 0G Storage blockchain network. It automates the process of uploading random images to the 0G Storage network using multiple wallet accounts and manages transactions on the blockchain.

## ✨ Features

- ✅ Support for multiple wallet private keys
- ✅ Proxy rotation for network requests
- ✅ Random image fetching from online sources
- ✅ File hash generation with uniqueness verification
- ✅ Automatic transaction handling
- ✅ Error management with retry mechanism
- ✅ Detailed colored console logging
- ✅ Multi-wallet processing

## 📋 Requirements

- Python 3.8 or higher
- An internet connection
- Valid 0G Storage wallet private keys
- (Optional) List of proxies for rotation

## 🚀 Installation

### For Windows

1. **Install Python**:
   - Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/windows/)
   - Ensure you check "Add Python to PATH" during installation

2. **Clone or download this repository**:
   ```
   git clone https://github.com/HexQuant-hub/0g-storage-scan-bot.git
   cd 0g-storage-scan-bot
   ```

3. **Create a virtual environment**:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

### For Linux

1. **Install Python and dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/HexQuant-hub/0g-storage-scan-bot.git
   cd 0g-storage-scan-bot
   ```

3. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Create a `.env` file** in the project root directory with your private keys:
   ```
   PRIVATE_KEY=0xyourprivatekeyhere
   PRIVATE_KEY_1=0xyourfirstprivatekeyhere
   PRIVATE_KEY_2=0xyoursecondprivatekeyhere
   PRIVATE_KEY_3=0xyourthirdprivatekeyhere
   ```

2. **(Optional) Create a `proxies.txt` file** with one proxy per line:
   ```
   http://username:password@ip:port
   http://ip:port
   ```

## 🔧 Usage

1. **Activate the virtual environment** (if not already activated):
   - Windows: `venv\Scripts\activate`
   - Linux: `source venv/bin/activate`

2. **Run the bot**:
   ```
   python main.py
   ```

3. **Follow the on-screen prompts**:
   - The bot will display available wallets
   - Enter the number of files to upload per wallet when prompted
   - The bot will handle the rest automatically

4. **Monitor the process**:
   - The console will display colorful logs showing progress
   - Each wallet will be processed sequentially
   - A summary will be shown at the end

## 🔍 Troubleshooting

- **Insufficient Balance Error**: Ensure your wallets have sufficient OG tokens for transactions (minimum 0.0015 OG)
- **Network Connection Issues**: Check your internet connection or try using proxies
- **Transaction Failures**: The bot will automatically retry failed transactions
- **Proxy Errors**: Verify your proxy format in `proxies.txt`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div dir="rtl">

# 0G Storage Scan Bot

![بنر](https://img.shields.io/badge/0G%20Storage-Scan%20Bot-blue?style=for-the-badge)
[![پایتون](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/downloads/)
[![مجوز](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


## ✨ ویژگی‌ها

- ✅ پشتیبانی از چندین کلید خصوصی کیف پول
- ✅ چرخش پروکسی برای درخواست‌های شبکه
- ✅ دریافت تصاویر تصادفی از منابع آنلاین
- ✅ تولید هش فایل با تأیید منحصربه‌فرد بودن
- ✅ مدیریت خودکار تراکنش‌ها
- ✅ مدیریت خطا با مکانیزم تلاش مجدد
- ✅ گزارش‌دهی کنسول رنگی با جزئیات
- ✅ پردازش چند کیف پول

## 📋 پیش‌نیازها

- پایتون ۳.۸ یا بالاتر
- اتصال به اینترنت
- کلیدهای خصوصی معتبر کیف پول 0G Storage
- (اختیاری) فهرستی از پروکسی‌ها برای چرخش

## 🚀 نصب و راه‌اندازی

### برای ویندوز

۱. **نصب پایتون**:
   - پایتون ۳.۸ یا بالاتر را از [python.org](https://www.python.org/downloads/windows/) دانلود و نصب کنید
   - مطمئن شوید که گزینه "Add Python to PATH" را هنگام نصب انتخاب کرده‌اید

۲. **کلون یا دانلود این مخزن**:
   ```
   git clone https://github.com/HexQuant-hub/0g-storage-scan-bot.git
   cd 0g-storage-scan-bot
   ```

۳. **ایجاد محیط مجازی**:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

۴. **نصب وابستگی‌ها**:
   ```
   pip install -r requirements.txt
   ```

### برای لینوکس

۱. **نصب پایتون و وابستگی‌ها**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

۲. **کلون مخزن**:
   ```bash
   git clone https://github.com/yourusername/0g-storage-scan-bot.git
   cd 0g-storage-scan-bot
   ```

۳. **ایجاد و فعال‌سازی محیط مجازی**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

۴. **نصب بسته‌های مورد نیاز**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ پیکربندی

۱. **ایجاد فایل `.env`** در دایرکتوری اصلی پروژه با کلیدهای خصوصی خود:
   ```
   PRIVATE_KEY=0xyourprivatekeyhere
   PRIVATE_KEY_1=0xyourfirstprivatekeyhere
   PRIVATE_KEY_2=0xyoursecondprivatekeyhere
   PRIVATE_KEY_3=0xyourthirdprivatekeyhere
   ```

۲. **(اختیاری) ایجاد فایل `proxies.txt`** با یک پروکسی در هر خط:
   ```
   http://username:password@ip:port
   http://ip:port
   ```

## 🔧 استفاده

۱. **فعال‌سازی محیط مجازی** (اگر قبلاً فعال نشده است):
   - ویندوز: `venv\Scripts\activate`
   - لینوکس: `source venv/bin/activate`

۲. **اجرای ربات**:
   ```
   python main.py
   ```

۳. **دنبال کردن راهنمایی‌های روی صفحه**:
   - ربات کیف پول‌های موجود را نمایش می‌دهد
   - تعداد فایل‌هایی که برای هر کیف پول آپلود می‌شود را وارد کنید
   - ربات به صورت خودکار بقیه فرآیند را انجام می‌دهد

۴. **نظارت بر فرآیند**:
   - کنسول گزارش‌های رنگی نمایش می‌دهد که پیشرفت را نشان می‌دهد
   - هر کیف پول به ترتیب پردازش می‌شود
   - در پایان خلاصه‌ای نمایش داده می‌شود

## 🔍 عیب‌یابی

- **خطای موجودی ناکافی**: اطمینان حاصل کنید که کیف پول‌های شما توکن‌های OG کافی برای تراکنش‌ها دارند (حداقل ۰.۰۰۱۵ OG)
- **مشکلات اتصال شبکه**: اتصال اینترنت خود را بررسی کنید یا از پروکسی‌ها استفاده کنید
- **شکست تراکنش‌ها**: ربات به طور خودکار تراکنش‌های ناموفق را دوباره امتحان می‌کند
- **خطاهای پروکسی**: فرمت پروکسی خود را در `proxies.txt` بررسی کنید

## 📄 مجوز

این پروژه تحت مجوز MIT است - برای جزئیات به فایل [LICENSE](LICENSE) مراجعه کنید.

</div>
