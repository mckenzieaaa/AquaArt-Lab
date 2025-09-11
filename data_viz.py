import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV数据
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"读取数据失败: {e}")
        return None

def plot_data(data, x_col, y_col, title="数据可视化", xlabel=None, ylabel=None):
    plt.figure(figsize=(10, 6))
    plt.plot(data[x_col], data[y_col], marker='o')
    plt.title(title)
    plt.xlabel(xlabel if xlabel else x_col)
    plt.ylabel(ylabel if ylabel else y_col)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    file_path = "data.csv"  # 请确保有data.csv文件
    data = load_data(file_path)
    if data is not None:
        # 假设有 '日期' 和 '数值' 两列
        plot_data(data, x_col='日期', y_col='数值', title="示例折线图", xlabel="日期", ylabel="数值")

if __name__ == "__main__":
    main()
