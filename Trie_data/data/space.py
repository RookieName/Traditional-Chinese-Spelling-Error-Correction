import json

input_file = "=球類.json"
output_file = "=球類.json"

try:
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. 將資料寫回新檔案，並加上換行與縮排
    # indent=4 代表每一層縮排 4 個空格；ensure_ascii=False 可以讓中文正常顯示不變成亂碼
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"處理成功！已將換行後的 JSON 儲存至：{output_file}")

except FileNotFoundError:
    print(f"錯誤：找不到檔案 '{input_file}'，請確認路徑是否正確。")
except json.JSONDecodeError:
    print("錯誤：該檔案不是合法的 JSON 格式。")