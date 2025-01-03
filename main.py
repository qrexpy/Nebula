import sys
import os
import configparser
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QGraphicsOpacityEffect
)
from PyQt6.QtGui import QPixmap, QIcon, QLinearGradient, QBrush, QColor, QPalette
from PyQt6.QtCore import Qt, QSize, QTimer

class NavButton(QPushButton):
    def __init__(self, text, icon_normal_path, icon_hover_path):
        super().__init__()
        self.setText(text)
        self.icon_normal = QIcon(icon_normal_path)
        self.icon_hover = QIcon(icon_hover_path)
        self.setIcon(self.icon_normal)
        self.setIconSize(QSize(24, 24))
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                text-align: left;
                padding: 5px 15px;
                font-size: 14px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
        """)

    def enterEvent(self, event):
        self.setIcon(self.icon_hover)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.icon_normal)
        super().leaveEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nebula")
        self.setWindowIcon(QIcon("Images/ic_launcher.ico"))
        self.setFixedSize(1000, 650)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        nav_panel = QWidget()
        nav_panel.setStyleSheet("background-color: #1a1a1a;")
        nav_panel.setFixedWidth(250)
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)

        profile_widget = QWidget()
        profile_widget.setStyleSheet("background-color: #444444;")
        profile_widget.setFixedHeight(160)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.setContentsMargins(10, 10, 10, 10)
        top_layout.setSpacing(10)

        pic_container = QWidget()
        pic_layout = QVBoxLayout(pic_container)
        pic_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pic_layout.setContentsMargins(0, 0, 0, 0)

        profile_pic = QLabel()
        pixmap = QPixmap("Images/normalpfp.png")
        scaled_pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        profile_pic.setPixmap(scaled_pixmap)
        profile_pic.setStyleSheet("border-radius: 0;")
        pic_layout.addWidget(profile_pic)

        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_layout.setContentsMargins(0, 0, 0, 0)

        self.profile_text = QLabel()
        self.profile_text.setStyleSheet("color: white; font-size: 14px; text-align: center;")
        text_layout.addWidget(self.profile_text)

        self.vip_label = QLabel()
        self.vip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_layout.addWidget(self.vip_label)

        self.id_label = QLabel()
        self.id_label.setStyleSheet("color: white; font-size: 14px; text-align: center;")
        text_layout.addWidget(self.id_label)

        top_layout.addWidget(pic_container)
        top_layout.addWidget(text_container)

        currency_layout = QHBoxLayout()
        currency_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        currency_layout.setSpacing(10)

        bcube_container = QWidget()
        bcube_container.setStyleSheet("background-color: #333333; border-radius: 5px;")
        bcube_box = QHBoxLayout(bcube_container)
        bcube_box.setContentsMargins(3, 3, 3, 3)

        bcube_icon = QLabel()
        bcube_pixmap = QPixmap("Images/bcube.png")
        bcube_scaled_pixmap = bcube_pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        bcube_icon.setPixmap(bcube_scaled_pixmap)
        bcube_box.addWidget(bcube_icon)

        bcube_label = QLabel("0")
        bcube_label.setStyleSheet("color: white; font-size: 14px; margin-left: 5px;")
        bcube_box.addWidget(bcube_label)

        gold_container = QWidget()
        gold_container.setStyleSheet("background-color: #333333; border-radius: 5px;")
        gold_box = QHBoxLayout(gold_container)
        gold_box.setContentsMargins(3, 3, 3, 3)

        gold_icon = QLabel()
        gold_pixmap = QPixmap("Images/gold.png")
        gold_scaled_pixmap = gold_pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        gold_icon.setPixmap(gold_scaled_pixmap)
        gold_box.addWidget(gold_icon)

        gold_label = QLabel("0")
        gold_label.setStyleSheet("color: white; font-size: 14px; margin-left: 5px;")
        gold_box.addWidget(gold_label)

        currency_layout.addWidget(bcube_container)
        currency_layout.addWidget(gold_container)

        profile_widget_layout = QVBoxLayout(profile_widget)
        profile_widget_layout.addLayout(top_layout)
        profile_widget_layout.addLayout(currency_layout)

        nav_layout.addWidget(profile_widget)

        buttons = [
            ("Game", "ic_game_nor.png", "ic_game_pre.png"),
            ("Dressing", "ic_dress_nor.png", "ic_dress_pre.png"),
            ("Clan", "ic_tribe_tab_nor.png", "ic_tribe_tab_pre.png"),
            ("Social", "ic_chat_nor.png", "ic_chat_pre.png")
        ]

        for text, nor, pre in buttons:
            btn = NavButton(text, f"Images/{nor}", f"Images/{pre}")
            nav_layout.addWidget(btn)
            btn.clicked.connect(self.clearContent)

        nav_layout.addStretch()

        more_btn = NavButton("More", "Images/ic_more_nor.png", "Images/ic_more_pre.png")
        nav_layout.addWidget(more_btn)

        self.main_layout.addWidget(nav_panel)

        self.content = QWidget()
        self.content.setStyleSheet("background-color: #1a1a1a;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.content)

        self.apply_config()

    def apply_config(self):
        config_path = "Config/user.cfg"
        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path)

            # Set the VIP level and image
            viplvl = config.getint("DEFAULT", "viplvl", fallback=1)
            vip_images = {
                1: "Images/vip.png",
                2: "Images/vipplus.png",
                3: "Images/mvp.png",
                4: "Images/mvpplus.png"
            }
            vip_image_path = vip_images.get(viplvl, "Images/vip.png")
            vip_pixmap = QPixmap(vip_image_path).scaled(60, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.vip_label.setPixmap(vip_pixmap)

            # Set the user ID
            user_id = config.get("DEFAULT", "id", fallback="256")
            self.id_label.setText(f"ID: {user_id}")

            # Set the username
            username = config.get("DEFAULT", "username", fallback="Null")
            self.profile_text.setText(username)

            # Apply color settings
            colorname = config.get("DEFAULT", "colorname", fallback="")
            if colorname == "rainbow":
                self.start_rainbow_animation()

    def start_rainbow_animation(self):
        self.current_r = 255
        self.current_g = 0
        self.current_b = 0
        self.increment = 1  # Step for changing color
        self.color_phase = 0  # Tracks which RGB phase is active
        self.rainbow_timer = QTimer(self)
        self.rainbow_timer.timeout.connect(self.update_rainbow_color)
        self.rainbow_timer.start(10)  # Adjust interval for smoothness

    def update_rainbow_color(self):
        if self.color_phase == 0:  # Red to Yellow (Increase Green)
            self.current_g += self.increment
            if self.current_g >= 255:
                self.current_g = 255
                self.color_phase = 1
        elif self.color_phase == 1:  # Yellow to Green (Decrease Red)
            self.current_r -= self.increment
            if self.current_r <= 0:
                self.current_r = 0
                self.color_phase = 2
        elif self.color_phase == 2:  # Green to Cyan (Increase Blue)
            self.current_b += self.increment
            if self.current_b >= 255:
                self.current_b = 255
                self.color_phase = 3
        elif self.color_phase == 3:  # Cyan to Blue (Decrease Green)
            self.current_g -= self.increment
            if self.current_g <= 0:
                self.current_g = 0
                self.color_phase = 4
        elif self.color_phase == 4:  # Blue to Magenta (Increase Red)
            self.current_r += self.increment
            if self.current_r >= 255:
                self.current_r = 255
                self.color_phase = 5
        elif self.color_phase == 5:  # Magenta to Red (Decrease Blue)
            self.current_b -= self.increment
            if self.current_b <= 0:
                self.current_b = 0
                self.color_phase = 0

        color = f"rgb({self.current_r}, {self.current_g}, {self.current_b})"
        self.profile_text.setStyleSheet(f"color: {color}; font-size: 14px; text-align: center;")

    def clearContent(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
