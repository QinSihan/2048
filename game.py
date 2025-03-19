import tkinter as tk
import random
import os
import json

# 颜色配置
GRID_COLOR = "#a39489"
EMPTY_CELL_COLOR = "#c2b3a9"
SCORE_LABEL_FONT = ("Verdana", 20)
SCORE_FONT = ("Helvetica", 32, "bold")
GAME_OVER_FONT = ("Helvetica", 48, "bold")
GAME_OVER_FONT_COLOR = "#ffffff"
WINNER_BG = "#ffcc00"
LOSER_BG = "#a39489"
BUTTON_FONT = ("Verdana", 12)
BUTTON_BG = "#8f7a66"
BUTTON_FG = "#ffffff"

CELL_COLORS = {
    2: "#fcefe6",
    4: "#f2e8cb",
    8: "#f5b682",
    16: "#f29446",
    32: "#ff775c",
    64: "#e64c2e",
    128: "#ede291",
    256: "#fce130",
    512: "#ffdb4a",
    1024: "#f0b922",
    2048: "#fad74d"
}

CELL_NUMBER_COLORS = {
    2: "#695c57",
    4: "#695c57",
    8: "#ffffff",
    16: "#ffffff",
    32: "#ffffff",
    64: "#ffffff",
    128: "#ffffff",
    256: "#ffffff",
    512: "#ffffff",
    1024: "#ffffff",
    2048: "#ffffff"
}

CELL_NUMBER_FONTS = {
    2: ("Helvetica", 55, "bold"),
    4: ("Helvetica", 55, "bold"),
    8: ("Helvetica", 55, "bold"),
    16: ("Helvetica", 50, "bold"),
    32: ("Helvetica", 50, "bold"),
    64: ("Helvetica", 50, "bold"),
    128: ("Helvetica", 45, "bold"),
    256: ("Helvetica", 45, "bold"),
    512: ("Helvetica", 45, "bold"),
    1024: ("Helvetica", 40, "bold"),
    2048: ("Helvetica", 40, "bold")
}

class Game(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # 创建数据目录
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self.grid()
        self.master.title('2048')
        
        # 加载最高分
        self.high_score = self.load_high_score()
        
        self.main_grid = tk.Frame(
            self, bg=GRID_COLOR, bd=3, width=400, height=400)
        self.main_grid.grid(pady=(80, 0))
        self.make_GUI()
        self.start_game()
        
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)
        self.master.bind("r", self.reset_game)  # 添加键盘快捷键R重置游戏
        self.master.bind("q", self.quit_game)   # 添加键盘快捷键Q退出游戏
        
        self.mainloop()
    
    def make_GUI(self):
        # 左侧重新开始按钮
        restart_button = tk.Button(
            self,
            text="restart",
            font=BUTTON_FONT,
            bg=BUTTON_BG,
            fg="#000000",  # 改为黑色文字
            command=self.reset_game
        )
        restart_button.place(relx=0.15, y=40, anchor="center")
        
        # 右侧退出按钮
        quit_button = tk.Button(
            self,
            text="quit",
            font=BUTTON_FONT,
            bg=BUTTON_BG,
            fg="#000000",  # 改为黑色文字
            command=self.quit_game
        )
        quit_button.place(relx=0.85, y=40, anchor="center")
        
        # 创建分数头部
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=40, anchor="center")
        
        # 当前分数
        tk.Label(
            score_frame,
            text="Score",
            font=SCORE_LABEL_FONT).grid(row=0, column=0, padx=20)
        self.score_label = tk.Label(score_frame, text="0", font=SCORE_FONT)
        self.score_label.grid(row=1, column=0)
        
        # 最高分
        tk.Label(
            score_frame,
            text="Best",
            font=SCORE_LABEL_FONT).grid(row=0, column=1, padx=20)
        self.high_score_label = tk.Label(score_frame, text=str(self.high_score), font=SCORE_FONT)
        self.high_score_label.grid(row=1, column=1)
        
        # 创建游戏网格
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=EMPTY_CELL_COLOR,
                    width=100,
                    height=100)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)
    
    def start_game(self):
        # 创建矩阵
        self.matrix = [[0] * 4 for _ in range(4)]
        
        # 初始化分数
        self.score = 0
        self.score_label.configure(text="0")
        
        # 初始添加两个2
        self.add_new_tile()
        self.add_new_tile()
        self.update_GUI()
    
    def add_new_tile(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        
        self.matrix[row][col] = random.choice([2, 4])
    
    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(
                        bg=CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=CELL_COLORS[cell_value],
                        fg=CELL_NUMBER_COLORS[cell_value],
                        font=CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value))
        
        self.score_label.configure(text=str(self.score))
        
        # 更新最高分
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.configure(text=str(self.high_score))
            self.save_high_score()
            
        self.update_idletasks()
    
    # 移动逻辑
    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix
    
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]
    
    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix
    
    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix
    
    # 移动方向
    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()
    
    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()
    
    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()
    
    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()
    
    # 检查游戏是否结束
    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False
    
    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False
    
    def game_over(self):
        if any(0 in row for row in self.matrix):
            return False
        
        if self.horizontal_move_exists() or self.vertical_move_exists():
            return False
        
        # 游戏结束
        game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # 游戏结束标签
        tk.Label(
            game_over_frame,
            text="Game Over!",
            bg=LOSER_BG,
            fg=GAME_OVER_FONT_COLOR,
            font=GAME_OVER_FONT).pack(pady=10)
        
        # 添加重新开始按钮到游戏结束框
        restart_button = tk.Button(
            game_over_frame,
            text="restart",
            font=BUTTON_FONT,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            command=self.reset_game
        )
        restart_button.pack(pady=10)
        
        return True
    
    # 新增方法：重置游戏
    def reset_game(self, event=None):
        # 清除可能存在的游戏结束框
        for widget in self.main_grid.winfo_children():
            if isinstance(widget, tk.Frame) and widget not in [cell["frame"] for row in self.cells for cell in row]:
                widget.destroy()
        
        self.start_game()
    
    # 新增方法：退出游戏
    def quit_game(self, event=None):
        self.master.destroy()
    
    # 新增方法：加载最高分
    def load_high_score(self):
        score_file = os.path.join(self.data_dir, "high_score.json")
        try:
            if os.path.exists(score_file):
                with open(score_file, "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except Exception as e:
            print(f"加载最高分时出错: {e}")
        return 0
    
    # 新增方法：保存最高分
    def save_high_score(self):
        score_file = os.path.join(self.data_dir, "high_score.json")
        try:
            with open(score_file, "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except Exception as e:
            print(f"保存最高分时出错: {e}")

def main():
    # 启动游戏
    root = tk.Tk()
    Game(root)

if __name__ == "__main__":
    main()