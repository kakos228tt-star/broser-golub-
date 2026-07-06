import sys
from PyQt6.QtCore import QUrl, Qt, QTimer, QObject, QEvent
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QTabWidget, QLabel, QMessageBox, QProgressBar
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

class AltF4Blocker(QObject):
    """Специальный фильтр для полной блокировки Alt+F4."""
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            # Проверяем, нажата ли F4 вместе с клавишей Alt
            if event.key() == Qt.Key.Key_F4 and (event.modifiers() & Qt.KeyboardModifier.AltModifier):
                return True # Говорим системе "игнорировать это нажатие"
        return super().eventFilter(obj, event)

class LoadingWindow(QWidget):
    def __init__(self, start_browser_callback):
        super().__init__()
        self.start_browser_callback = start_browser_callback
        self.progress_value = 0
        self.tips = [
            "Совет: Голубь-браузер — лучший выбор для геймеров и про-игроков!",
            "Совет: Включение приватности скрывает ваши следы в сети.",
            "Совет: Наш кастомный крестик защитит ваши вкладки от случайного закрытия.",
            "Совет: Не выключайте браузер во время важной катки!"
        ]
        self.tip_index = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.resize(500, 300)
        self.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4; font-family: Arial;")

        layout = QVBoxLayout()
        self.title_label = QLabel("СИСТЕМА: Браузер Голубь запущен!", self)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #89b4fa;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("""
            QProgressBar { border: 2px solid #89b4fa; border-radius: 5px; text-align: center; }
            QProgressBar::chunk { background-color: #89b4fa; }
        """)
        
        self.tip_label = QLabel(self.tips[0], self)
        self.tip_label.setWordWrap(True)
        self.tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tip_label.setStyleSheet("color: #a6adc8; font-style: italic;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.tip_label)
        self.setLayout(layout)

        QTimer.singleShot(1000, self.start_loading)

    def start_loading(self):
        self.title_label.setText("Загрузка компонентов Голубь-Браузера...")
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(100)

        self.tip_timer = QTimer()
        self.tip_timer.timeout.connect(self.change_tip)
        self.tip_timer.start(2500)

    def update_progress(self):
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.progress_timer.stop()
            self.tip_timer.stop()
            self.close()
            self.start_browser_callback()

    def change_tip(self):
        self.tip_index = (self.tip_index + 1) % len(self.tips)
        self.tip_label.setText(self.tips[self.tip_index])

class GolubBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.privacy_mode = False
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #181825; color: #cdd6f4; font-family: Arial;")

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #11111b; height: 40px;")
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(10, 0, 10, 0)

        title = QLabel("🐦 Голубь Браузер (Геймерский)")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.close_btn = QPushButton("❌")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton { background-color: #f38ba8; border-radius: 5px; color: #11111b; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #ffa5b5; }
        """)
        self.close_btn.clicked.connect(self.confirm_exit)

        top_bar_layout.addWidget(title)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.close_btn)
        top_bar.setLayout(top_bar_layout)

        nav_bar = QWidget()
        nav_bar.setStyleSheet("background-color: #1e1e2e; padding: 5px;")
        nav_layout = QHBoxLayout()

        self.addr_bar = QLineEdit()
        self.addr_bar.setStyleSheet("background-color: #313244; color: #cdd6f4; border: 1px solid #45475a; border-radius: 4px; padding: 4px;")
        self.addr_bar.returnPressed.connect(self.load_url)

        go_btn = QPushButton("Перейти")
        go_btn.setStyleSheet("background-color: #89b4fa; color: #11111b; padding: 5px 10px; border-radius: 4px; border: none; font-weight: bold;")
        go_btn.clicked.connect(self.load_url)

        add_tab_btn = QPushButton("+ Вкладка")
        add_tab_btn.setStyleSheet("background-color: #a6e3a1; color: #11111b; padding: 5px 10px; border-radius: 4px; border: none; font-weight: bold;")
        add_tab_btn.clicked.connect(lambda: self.add_new_tab())

        self.privacy_btn = QPushButton("Приватность: ВЫКЛ")
        self.privacy_btn.setStyleSheet("background-color: #f9e2af; color: #11111b; padding: 5px 10px; border-radius: 4px; border: none; font-weight: bold;")
        self.privacy_btn.clicked.connect(self.toggle_privacy)

        nav_layout.addWidget(self.addr_bar)
        nav_layout.addWidget(go_btn)
        nav_layout.addWidget(add_tab_btn)
        nav_layout.addWidget(self.privacy_btn)
        nav_bar.setLayout(nav_layout)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setStyleSheet("""
            QTabWidget::panel { border: none; }
            QTabBar::tab { background: #313244; color: #cdd6f4; padding: 8px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: #1e1e2e; font-weight: bold; }
        """)

        main_layout.addWidget(top_bar)
        main_layout.addWidget(nav_bar)
        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.add_new_tab("https://google.com")

    def add_new_tab(self, url_str="https://google.com", label="Новая вкладка"):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url_str))
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_address_bar(qurl, browser))
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            QMessageBox.information(self, "Голубь", "Нельзя закрыть последнюю вкладку!")

    def load_url(self):
        url = self.addr_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))

    def update_address_bar(self, qurl, browser):
        if browser == self.tabs.currentWidget():
            self.addr_bar.setText(qurl.toString())

    def toggle_privacy(self):
        self.privacy_mode = not self.privacy_mode
        if self.privacy_mode:
            self.privacy_btn.setText("Приватность: ВКЛ")
            self.privacy_btn.setStyleSheet("background-color: #cba6f7; color: #11111b; padding: 5px 10px; border-radius: 4px; border: none; font-weight: bold;")
            self.add_new_tab("https://duckduckgo.com", "Аноним 🥷")
        else:
            self.privacy_btn.setText("Приватность: ВЫКЛ")
            self.privacy_btn.setStyleSheet("background-color: #f9e2af; color: #11111b; padding: 5px 10px; border-radius: 4px; border: none; font-weight: bold;")

    def confirm_exit(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Предупреждение системы")
        msg_box.setText("Вы действительно хотите выйти?\nВы можете потерять весь игровой прогресс, и Голубь очень расстроится! 🐦🥺")
        msg_box.setStyleSheet("""
            QMessageBox { background-color: #1e1e2e; color: #cdd6f4; font-family: Arial; font-size: 14px; }
            QPushButton { background-color: #89b4fa; color: #11111b; padding: 6px 15px; border-radius: 4px; font-weight: bold; min-width: 80px; border: none; }
            QPushButton:hover { background-color: #b4befe; }
        """)
        exit_button = msg_box.addButton("Выйти", QMessageBox.ButtonRole.YesRole)
        keep_button = msg_box.addButton("Продолжить", QMessageBox.ButtonRole.NoRole)
        msg_box.exec()
        if msg_box.clickedButton() == exit_button:
            sys.exit(0)

def run_app():
    app = QApplication(sys.argv)
    
    # Создаем и устанавливаем глобальный блокировщик Alt+F4 на всё приложение
    blocker = AltF4Blocker()
    app.installEventFilter(blocker)

    def show_browser():
        global browser_window
        browser_window = GolubBrowser()
        browser_window.show()

    loading_window = LoadingWindow(start_browser_callback=show_browser)
    loading_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
