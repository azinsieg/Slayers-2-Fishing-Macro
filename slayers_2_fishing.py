

import cv2
import numpy as np
import time
import signal
import sys
import ctypes
import os
import json
from datetime import datetime

import mss
import keyboard

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QGroupBox, QGridLayout, QDialog, QMessageBox, QCheckBox,
    QDialogButtonBox
)

from PyQt5.QtCore import (
    Qt, pyqtSignal, QThread
)

from PyQt5.QtGui import (
    QFont, QMovie, QPixmap, QIcon
)






GEOMETRY = None

FPS = 30

YELLOW_LOWER = np.array([15, 40, 60])
YELLOW_UPPER = np.array([45, 255, 255])

GREEN_LOWER = np.array([35, 30, 40])
GREEN_UPPER = np.array([95, 255, 255])

WHITE_LOWER = np.array([0, 0, 150])
WHITE_UPPER = np.array([180, 80, 255])

DEADZONE = 4
BRAKE_ZONE = 28
PREDICTION = 0.80








LOST_TIMEOUT = 2.0

T_HOLD_TIME = 4.0


CAST_DELAY = 0.5
RECAST_DELAY = 0.5


CAST_TIMEOUT = 7

CLICK_HOLD_TIME = 0.08













MINIGAME_DETECTION_DELAY = 6


WAIT_BEFORE_T_HOLD = 0.0



MINIGAME_CONFIRM_FRAMES = 3


RETRY_DELAY = 0.5







MINIMAL_LOGS = True
MINIMALIST_MODE = False

MINIMALIST_COLOR = "Roxo escuro"

BACKGROUND_COLORS = {
    "Roxo escuro": "#160022",
    "Preto": "#050505",
    "Vermelho": "#300000",
    "Azul": "#00152e",
    "Verde": "#002510"
}






def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(
            os.path.abspath(__file__)
        )

    return os.path.join(
        base_path,
        relative_path
    )






LANGUAGE = "pt"

LANGUAGES = {
    "pt": "Português",
    "en": "English",
    "zh": "中文"
}


def get_settings_path():
    base = os.environ.get("APPDATA") or os.path.join(
        os.path.expanduser("~"),
        "AppData",
        "Roaming"
    )
    folder = os.path.join(base, "Slayer2Fishing")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "settings.json")


def load_settings():
    global FPS
    global DEADZONE
    global BRAKE_ZONE
    global PREDICTION
    global CAST_TIMEOUT
    global MINIGAME_DETECTION_DELAY
    global WAIT_BEFORE_T_HOLD
    global MINIMAL_LOGS
    global MINIMALIST_MODE
    global MINIMALIST_COLOR
    global LANGUAGE

    try:
        with open(get_settings_path(), "r", encoding="utf-8") as file:
            data = json.load(file)

        FPS = int(data.get("fps", FPS))
        DEADZONE = int(data.get("deadzone", DEADZONE))
        BRAKE_ZONE = int(data.get("brake_zone", BRAKE_ZONE))
        PREDICTION = float(data.get("prediction", PREDICTION))
        CAST_TIMEOUT = int(data.get("cast_timeout", CAST_TIMEOUT))
        MINIGAME_DETECTION_DELAY = int(data.get("detection_delay", MINIGAME_DETECTION_DELAY))
        WAIT_BEFORE_T_HOLD = float(data.get("wait_before_t", WAIT_BEFORE_T_HOLD))
        MINIMAL_LOGS = bool(data.get("minimal_logs", MINIMAL_LOGS))
        MINIMALIST_MODE = bool(data.get("minimalist_mode", MINIMALIST_MODE))
        MINIMALIST_COLOR = str(data.get("minimalist_color", MINIMALIST_COLOR))
        LANGUAGE = str(data.get("language", LANGUAGE))

        FPS = max(10, min(60, FPS))
        DEADZONE = max(1, min(20, DEADZONE))
        BRAKE_ZONE = max(1, min(50, BRAKE_ZONE))
        PREDICTION = max(0.0, min(1.0, PREDICTION))
        CAST_TIMEOUT = max(1, min(30, CAST_TIMEOUT))
        MINIGAME_DETECTION_DELAY = max(1, min(30, MINIGAME_DETECTION_DELAY))
        WAIT_BEFORE_T_HOLD = max(0.0, min(30.0, WAIT_BEFORE_T_HOLD))

        if LANGUAGE not in LANGUAGES:
            LANGUAGE = "pt"
        if MINIMALIST_COLOR not in BACKGROUND_COLORS:
            MINIMALIST_COLOR = "Roxo escuro"
    except Exception:
        pass


def save_settings():
    data = {
        "fps": FPS,
        "deadzone": DEADZONE,
        "brake_zone": BRAKE_ZONE,
        "prediction": PREDICTION,
        "cast_timeout": CAST_TIMEOUT,
        "detection_delay": MINIGAME_DETECTION_DELAY,
        "wait_before_t": WAIT_BEFORE_T_HOLD,
        "minimal_logs": MINIMAL_LOGS,
        "minimalist_mode": MINIMALIST_MODE,
        "minimalist_color": MINIMALIST_COLOR,
        "language": LANGUAGE
    }

    try:
        with open(get_settings_path(), "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception:
        pass


load_settings()

TRANSLATIONS = {
    "pt": {
        "Slayer 2 Fishing by nilec2 & siegjf": "Slayer 2 Fishing by nilec2 & siegjf",
        "⚙ Configurações": "⚙ Configurações",
        "Configurações": "Configurações",
        "Status": "Status",
        "Hotkeys": "Hotkeys",
        "Iniciar:": "Iniciar:",
        "Parar:": "Parar:",
        "Extras:": "Extras:",
        "Ctrl+C / Esc": "Ctrl+C / Esc",
        "Selecionar Região": "Selecionar Região",
        "▶ Iniciar": "▶ Iniciar",
        "Parar": "Parar",
        "FPS:": "FPS:",
        "Deadzone:": "Deadzone:",
        "Brake Zone:": "Brake Zone:",
        "Prediction:": "Prediction:",
        "Cast Timeout (s):": "Cast Timeout (s):",
        "Espera Detectar (s):": "Espera Detectar (s):",
        "Espera T (s):": "Espera T (s):",
        "🗑 Limpar Logs": "🗑 Limpar Logs",
        "Logs": "Logs",
        "⚙": "⚙",
        "Log Detalhado": "Log Detalhado",
        "Mostra logs de cada frame. Desativado = logs minimalistas.": "Mostra logs de cada frame. Desativado = logs minimalistas.",
        "Minimalist Mode": "Minimalist Mode",
        "Cor do programa:": "Cor do programa:",
        "No Minimalist Mode, a GIF/imagem de fundo fica desativada.": "No Minimalist Mode, a GIF/imagem de fundo fica desativada.",
        "Aviso": "Aviso",
        "Selecione a região primeiro!": "Selecione a região primeiro!",
        "Configurações": "Configurações",
        "Tempo máximo procurando o minigame após lançamento": "Tempo máximo procurando o minigame após lançamento",
        "Tempo que aguarda antes de detectar o minigame": "Tempo que aguarda antes de detectar o minigame",
        "Tempo que aguarda antes de segurar T": "Tempo que aguarda antes de segurar T",
        "PARADO": "PARADO",
        "FISHING": "FISHING",
        "T HOLD": "T HOLD",
        "LOST TARGET": "LOST TARGET",
        "STOPPED": "STOPPED",
        "AGUARDANDO MINIGAME": "AGUARDANDO MINIGAME",
        "DOWN": "DOWN",
        "UP": "UP",
        "HOLD": "HOLD",
        "RELEASE": "RELEASE",
        "KEEP": "KEEP",
        "Roxo escuro": "Roxo escuro",
        "Preto": "Preto",
        "Vermelho": "Vermelho",
        "Azul": "Azul",
        "Verde": "Verde",
        "Idioma:": "Idioma:",
        "Português": "Português",
        "English": "English",
        "中文": "中文"
    },
    "en": {
        "Slayer 2 Fishing by nilec2 & siegjf": "Slayer 2 Fishing by nilec2 & siegjf",
        "⚙ Configurações": "⚙ Settings",
        "Configurações": "Settings",
        "Status": "Status",
        "Hotkeys": "Hotkeys",
        "Iniciar:": "Start:",
        "Parar:": "Stop:",
        "Extras:": "Extras:",
        "Ctrl+C / Esc": "Ctrl+C / Esc",
        "Selecionar Região": "Select Region",
        "▶ Iniciar": "▶ Start",
        "Parar": "Stop",
        "FPS:": "FPS:",
        "Deadzone:": "Deadzone:",
        "Brake Zone:": "Brake Zone:",
        "Prediction:": "Prediction:",
        "Cast Timeout (s):": "Cast Timeout (s):",
        "Espera Detectar (s):": "Detection Delay (s):",
        "Espera T (s):": "Wait T (s):",
        "🗑 Limpar Logs": "🗑 Clear Logs",
        "Logs": "Logs",
        "⚙": "⚙",
        "Log Detalhado": "Detailed Logs",
        "Mostra logs de cada frame. Desativado = logs minimalistas.": "Shows logs from every frame. Disabled = minimal logs.",
        "Minimalist Mode": "Minimalist Mode",
        "Cor do programa:": "Program color:",
        "No Minimalist Mode, a GIF/imagem de fundo fica desativada.": "In Minimalist Mode, the GIF/background image is disabled.",
        "Aviso": "Warning",
        "Selecione a região primeiro!": "Select the region first!",
        "Tempo máximo procurando o minigame após lançamento": "Maximum time searching for the minigame after casting",
        "Tempo que aguarda antes de detectar o minigame": "Time to wait before detecting the minigame",
        "Tempo que aguarda antes de segurar T": "Time to wait before holding T",
        "PARADO": "STOPPED",
        "FISHING": "FISHING",
        "T HOLD": "T HOLD",
        "LOST TARGET": "LOST TARGET",
        "STOPPED": "STOPPED",
        "AGUARDANDO MINIGAME": "WAITING FOR MINIGAME",
        "DOWN": "DOWN",
        "UP": "UP",
        "HOLD": "HOLD",
        "RELEASE": "RELEASE",
        "KEEP": "KEEP",
        "Roxo escuro": "Dark Purple",
        "Preto": "Black",
        "Vermelho": "Red",
        "Azul": "Blue",
        "Verde": "Green",
        "Idioma:": "Language:",
        "Português": "Portuguese",
        "English": "English",
        "中文": "Chinese"
    },
    "zh": {
        "Slayer 2 Fishing by nilec2 & siegjf": "Slayer 2 Fishing by nilec2 & siegjf",
        "⚙ Configurações": "⚙ 设置",
        "Configurações": "设置",
        "Status": "状态",
        "Hotkeys": "快捷键",
        "Iniciar:": "开始：",
        "Parar:": "停止：",
        "Extras:": "其他：",
        "Ctrl+C / Esc": "Ctrl+C / Esc",
        "Selecionar Região": "选择区域",
        "▶ Iniciar": "▶ 开始",
        "Parar": "停止",
        "FPS:": "FPS：",
        "Deadzone:": "死区：",
        "Brake Zone:": "刹车区：",
        "Prediction:": "预测：",
        "Cast Timeout (s):": "抛竿超时（秒）：",
        "Espera Detectar (s):": "检测等待（秒）：",
        "Espera T (s):": "按住 T 前等待（秒）：",
        "🗑 Limpar Logs": "🗑 清除日志",
        "Logs": "日志",
        "⚙": "⚙",
        "Log Detalhado": "详细日志",
        "Mostra logs de cada frame. Desativado = logs minimalistas.": "显示每一帧的日志。关闭后使用简洁日志。",
        "Minimalist Mode": "简洁模式",
        "Cor do programa:": "程序颜色：",
        "No Minimalist Mode, a GIF/imagem de fundo fica desativada.": "简洁模式下将禁用 GIF/背景图片。",
        "Aviso": "警告",
        "Selecione a região primeiro!": "请先选择区域！",
        "Tempo máximo procurando o minigame após lançamento": "抛竿后寻找小游戏的最长时间",
        "Tempo que aguarda antes de detectar o minigame": "检测小游戏前等待的时间",
        "Tempo que aguarda antes de segurar T": "按住 T 前的等待时间",
        "PARADO": "已停止",
        "FISHING": "钓鱼中",
        "T HOLD": "按住 T",
        "LOST TARGET": "目标丢失",
        "STOPPED": "已停止",
        "AGUARDANDO MINIGAME": "等待小游戏",
        "DOWN": "按下",
        "UP": "松开",
        "HOLD": "按住",
        "RELEASE": "松开",
        "KEEP": "保持",
        "Roxo escuro": "深紫色",
        "Preto": "黑色",
        "Vermelho": "红色",
        "Azul": "蓝色",
        "Verde": "绿色",
        "Idioma:": "语言：",
        "Português": "葡萄牙语",
        "English": "英语",
        "中文": "中文"
    }
}


def tr(text):
    return TRANSLATIONS.get(LANGUAGE, TRANSLATIONS["pt"]).get(text, text)


def translate_runtime_text(text):
    result = str(text)
    table = TRANSLATIONS.get(LANGUAGE, TRANSLATIONS["pt"])

    
    for source, target in sorted(table.items(), key=lambda item: len(item[0]), reverse=True):
        if source and source in result:
            result = result.replace(source, target)

    
    fragments = {
        "en": {
            "[INFO] Selecione a região...": "[INFO] Select the region...",
            "[ERRO] Seleção cancelada": "[ERROR] Selection cancelled",
            "[ERRO] Região inválida": "[ERROR] Invalid region",
            "[OK] Região selecionada:": "[OK] Region selected:",
            "[ERRO] Nenhuma região selecionada!": "[ERROR] No region selected!",
            "[INFO] Bot iniciado em ": "[INFO] Bot started at ",
            "[INFO] Bot iniciado.": "[INFO] Bot started.",
            "[INFO] Bot parado": "[INFO] Bot stopped",
            "[INFO] Jogando a vara...": "[INFO] Casting the rod...",
            "[INFO] Vara lançada!": "[INFO] Rod cast!",
            "[INFO] Tentando lançar ": "[INFO] Trying to cast ",
            "[INFO] NÃO procurando minigame durante ": "[INFO] NOT detecting the minigame for ",
            "[INFO] Agora procurando ": "[INFO] Now searching ",
            "[INFO] Tempo de espera concluído.": "[INFO] Waiting period completed.",
            "[OK] Minigame confirmado!": "[OK] Minigame confirmed!",
            "[OK] Minigame detectado novamente.": "[OK] Minigame detected again.",
            "[INFO] Minigame desapareceu por tempo demais.": "[INFO] Minigame disappeared for too long.",
            "[INFO] Finalizando esta tentativa e preparando novo lançamento...": "[INFO] Ending this attempt and preparing a new cast...",
            "[AVISO] Minigame desapareceu...": "[WARNING] Minigame disappeared...",
            "[AVISO] Minigame desaparecido há ": "[WARNING] Minigame missing for ",
            "[AVISO] Minigame não apareceu.": "[WARNING] Minigame did not appear.",
            "[AVISO] Erro recuperável. Tentando novamente...": "[WARNING] Recoverable error. Trying again...",
            "[ERRO] ": "[ERROR] ",
            "[INFO] Aguardando ": "[INFO] Waiting ",
            "s antes de segurar T...": "s before holding T...",
            "[INFO] Segurando T...": "[INFO] Holding T...",
            "[OK] T concluído": "[OK] T completed",
            "[INFO] Minigame desapareceu ": "[INFO] Minigame disappeared "
        },
        "zh": {
            "[INFO] Selecione a região...": "[信息] 请选择区域……",
            "[ERRO] Seleção cancelada": "[错误] 已取消选择",
            "[ERRO] Região inválida": "[错误] 区域无效",
            "[OK] Região selecionada:": "[成功] 已选择区域：",
            "[ERRO] Nenhuma região selecionada!": "[错误] 尚未选择区域！",
            "[INFO] Bot iniciado em ": "[信息] 机器人启动于 ",
            "[INFO] Bot iniciado.": "[信息] 机器人已启动。",
            "[INFO] Bot parado": "[信息] 机器人已停止",
            "[INFO] Jogando a vara...": "[信息] 正在抛竿……",
            "[INFO] Vara lançada!": "[信息] 已抛竿！",
            "[INFO] Tentando lançar ": "[信息] 尝试抛竿 ",
            "[INFO] NÃO procurando minigame ": "[信息] 暂不检测小游戏，等待 ",
            "[INFO] Agora procurando ": "[信息] 现在开始寻找 ",
            "[INFO] Tempo de espera concluído.": "[信息] 等待结束。",
            "[OK] Minigame confirmado!": "[成功] 小游戏已确认！",
            "[OK] Minigame detectado novamente.": "[成功] 再次检测到小游戏。",
            "[INFO] Minigame desapareceu por tempo demais.": "[信息] 小游戏消失时间过长。",
            "[INFO] Finalizando esta tentativa e preparando novo lançamento...": "[信息] 结束本次尝试并准备重新抛竿……",
            "[AVISO] Minigame desapareceu...": "[警告] 小游戏消失……",
            "[AVISO] Minigame desaparecido há ": "[警告] 小游戏已消失 ",
            "[AVISO] Minigame não apareceu.": "[警告] 小游戏没有出现。",
            "[AVISO] Erro recuperável. Tentando novamente...": "[警告] 可恢复错误。正在重试……",
            "[ERRO] ": "[错误] ",
            "[信息] 等待 ": "[信息] 等待 ",
            "s antes de segurar T...": "秒后按住 T……",
            "[INFO] Segurando T...": "[信息] 正在按住 T……",
            "[OK] T concluído": "[成功] T 操作完成",
            "[INFO] Minigame desapareceu ": "[信息] 小游戏消失 "
        }
    }

    if LANGUAGE in fragments:
        for source, target in sorted(fragments[LANGUAGE].items(), key=lambda item: len(item[0]), reverse=True):
            result = result.replace(source, target)

    return result


def mark_i18n_widgets(root):
    from PyQt5.QtWidgets import QLabel, QPushButton, QGroupBox, QCheckBox, QComboBox

    for widget in root.findChildren(QWidget):
        if isinstance(widget, QGroupBox):
            text = widget.title()
            if text:
                widget.setProperty("i18n_source", text)
        elif isinstance(widget, (QLabel, QPushButton, QCheckBox)):
            text = widget.text()
            if text:
                widget.setProperty("i18n_source", text)

        tooltip = widget.toolTip()
        if tooltip:
            widget.setProperty("i18n_tooltip_source", tooltip)

        if isinstance(widget, QComboBox):
            sources = [widget.itemText(i) for i in range(widget.count())]
            widget.setProperty("i18n_items", sources)


def apply_i18n_widgets(root):
    from PyQt5.QtWidgets import QLabel, QPushButton, QGroupBox, QCheckBox, QComboBox, QDialogButtonBox

    if isinstance(root, QDialog):
        root.setWindowTitle(tr("⚙ Configurações"))
    elif isinstance(root, QMainWindow):
        root.setWindowTitle(tr("Slayer 2 Fishing by nilec2 & siegjf"))

    for widget in root.findChildren(QWidget):
        source = widget.property("i18n_source")

        tooltip_source = widget.property("i18n_tooltip_source")
        if tooltip_source:
            widget.setToolTip(tr(str(tooltip_source)))
        if source:
            if isinstance(widget, QGroupBox):
                widget.setTitle(tr(str(source)))
            elif isinstance(widget, (QLabel, QPushButton, QCheckBox)):
                widget.setText(tr(str(source)))

        if isinstance(widget, QComboBox):
            sources = widget.property("i18n_items")
            if sources:
                current = widget.currentIndex()
                widget.blockSignals(True)
                widget.clear()
                widget.addItems([tr(str(x)) for x in sources])
                if current >= 0 and current < widget.count():
                    widget.setCurrentIndex(current)
                widget.blockSignals(False)

        if isinstance(widget, QDialogButtonBox):
            ok = widget.button(QDialogButtonBox.Ok)
            cancel = widget.button(QDialogButtonBox.Cancel)
            if ok:
                ok.setText({"pt": "OK", "en": "OK", "zh": "确定"}.get(LANGUAGE, "OK"))
            if cancel:
                cancel.setText({"pt": "Cancelar", "en": "Cancel", "zh": "取消"}.get(LANGUAGE, "Cancel"))






mouse_held = False

previous_target_y = None
previous_player_y = None

target_velocity = 0.0
player_velocity = 0.0

lost_since = None






user32 = ctypes.windll.user32

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008






class MOUSEINPUT(ctypes.Structure):

    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class KEYBDINPUT(ctypes.Structure):

    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class HARDWAREINPUT(ctypes.Structure):

    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_ushort),
        ("wParamH", ctypes.c_ushort),
    ]


class INPUT_UNION(ctypes.Union):

    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):

    _anonymous_ = ("union",)

    _fields_ = [
        ("type", ctypes.c_ulong),
        ("union", INPUT_UNION),
    ]






def send_input(input_event):

    size = ctypes.sizeof(INPUT)

    result = user32.SendInput(
        1,
        ctypes.byref(input_event),
        size
    )

    if result != 1:
        raise ctypes.WinError()






def mouse_down():

    event = INPUT()

    event.type = INPUT_MOUSE

    event.mi = MOUSEINPUT(
        0,
        0,
        0,
        MOUSEEVENTF_LEFTDOWN,
        0,
        None
    )

    send_input(event)


def mouse_up():

    event = INPUT()

    event.type = INPUT_MOUSE

    event.mi = MOUSEINPUT(
        0,
        0,
        0,
        MOUSEEVENTF_LEFTUP,
        0,
        None
    )

    send_input(event)


def click_mouse():

    release_mouse()

    mouse_down()

    time.sleep(
        CLICK_HOLD_TIME
    )

    mouse_up()


def hold_mouse():

    global mouse_held

    if mouse_held:
        return

    mouse_down()

    mouse_held = True


def release_mouse():

    global mouse_held

    if mouse_held:

        mouse_up()

    mouse_held = False






T_SCANCODE = 0x14


def key_down(scancode):

    event = INPUT()

    event.type = INPUT_KEYBOARD

    event.ki = KEYBDINPUT(
        0,
        scancode,
        KEYEVENTF_SCANCODE,
        0,
        None
    )

    send_input(event)


def key_up(scancode):

    event = INPUT()

    event.type = INPUT_KEYBOARD

    event.ki = KEYBDINPUT(
        0,
        scancode,
        KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP,
        0,
        None
    )

    send_input(event)


def hold_t():

    key_down(T_SCANCODE)

    time.sleep(
        T_HOLD_TIME
    )

    key_up(T_SCANCODE)






def cleanup():

    release_mouse()

    try:

        key_up(
            T_SCANCODE
        )

    except Exception:
        pass






sct = mss.mss()


def capture():

    frame = np.array(
        sct.grab(
            GEOMETRY
        )
    )

    return cv2.cvtColor(
        frame,
        cv2.COLOR_BGRA2BGR
    )






def find_center(mask):

    kernel = np.ones(
        (3, 3),
        np.uint8
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candidates = []

    for contour in contours:

        area = cv2.contourArea(
            contour
        )

        if area < 5:
            continue

        x, y, w, h = cv2.boundingRect(
            contour
        )

        ratio = (
            w / h
            if h
            else 0
        )

        if 0.4 <= ratio <= 2.5:

            center_y = (
                y + h // 2
            )

            candidates.append(
                (
                    area,
                    center_y,
                    w,
                    h
                )
            )

    if not candidates:
        return None

    candidates.sort(
        reverse=True
    )

    return candidates[0]


def find_target(frame):

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )

    yellow = cv2.inRange(
        hsv,
        YELLOW_LOWER,
        YELLOW_UPPER
    )

    green = cv2.inRange(
        hsv,
        GREEN_LOWER,
        GREEN_UPPER
    )

    mask = cv2.bitwise_or(
        yellow,
        green
    )

    return find_center(
        mask
    )


def find_player(frame):

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )

    white = cv2.inRange(
        hsv,
        WHITE_LOWER,
        WHITE_UPPER
    )

    return find_center(
        white
    )






def detect_minigame():

    frame = capture()

    target = find_target(
        frame
    )

    player = find_player(
        frame
    )

    return (
        target is not None
        and
        player is not None
    )






def update_velocity(
    target_y,
    player_y
):

    global previous_target_y
    global previous_player_y
    global target_velocity
    global player_velocity

    if previous_target_y is None:

        previous_target_y = target_y
        previous_player_y = player_y

        return

    target_delta = (
        target_y
        -
        previous_target_y
    )

    player_delta = (
        player_y
        -
        previous_player_y
    )

    target_velocity = (
        target_velocity * 0.65
        +
        target_delta * 0.35
    )

    player_velocity = (
        player_velocity * 0.65
        +
        player_delta * 0.35
    )

    previous_target_y = target_y
    previous_player_y = player_y






def control(
    target_y,
    player_y
):

    difference = (
        target_y
        -
        player_y
    )

    predicted_player = (
        player_y
        +
        player_velocity
        *
        PREDICTION
    )

    predicted_difference = (
        target_y
        -
        predicted_player
    )

    if (
        predicted_difference < -BRAKE_ZONE
        or
        predicted_difference < -DEADZONE
    ):

        hold_mouse()

        return (
            "HOLD",
            difference,
            predicted_difference
        )

    if (
        predicted_difference > BRAKE_ZONE
        or
        predicted_difference > DEADZONE
    ):

        release_mouse()

        return (
            "RELEASE",
            difference,
            predicted_difference
        )

    return (
        "KEEP",
        difference,
        predicted_difference
    )






def reset_tracking():

    global previous_target_y
    global previous_player_y
    global target_velocity
    global player_velocity

    previous_target_y = None
    previous_player_y = None

    target_velocity = 0.0
    player_velocity = 0.0






class BotThread(QThread):

    log_signal = pyqtSignal(str)

    status_signal = pyqtSignal(str)

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.running = False

        self.cast_count = 0

    
    
    

    def log(
        self,
        message
    ):

        if MINIMAL_LOGS:

            if (
                message.startswith(
                    "Alvo="
                )
                or
                message.startswith(
                    "[AVISO] Minigame desaparecido"
                )
            ):

                return

        self.log_signal.emit(
            translate_runtime_text(message)
        )

    
    
    

    def run(self):

        global GEOMETRY

        self.running = True

        if GEOMETRY is None:

            self.log(
                "[ERRO] Nenhuma região selecionada!"
            )

            self.running = False

            return

        self.log(
            f"[INFO] Região selecionada: "
            f"{GEOMETRY}"
        )

        self.log(
            f"[INFO] Configurações: "
            f"FPS={FPS}, "
            f"Deadzone={DEADZONE}px, "
            f"Brake={BRAKE_ZONE}px"
        )

        self.log(
            "[INFO] Bot iniciado."
        )

        self.log(
            f"[INFO] Espera após lançamento: "
            f"{MINIGAME_DETECTION_DELAY:.1f}s"
        )

        
        
        

        while self.running:

            try:

                self.cast_count += 1

                self.log(
                    f"\n[INFO]... "
                    f"{self.cast_count}..."
                )

                self.status_signal.emit(
                    f"CAST #{self.cast_count}"
                )

                
                
                

                release_mouse()

                reset_tracking()

                
                
                

                self.log(
                    "[INFO] Jogando a vara..."
                )

                click_mouse()

                if not self.running:
                    break

                
                
                

                self.log(
                    "[INFO] Vara lançada!"
                )

                self.log(
                    "[INFO] NÃO procurando minigame "
                    f" {MINIGAME_DETECTION_DELAY:.1f}s..."
                )

                self.status_signal.emit(
                    "AGUARDANDO MINIGAME"
                )

                wait_start = time.monotonic()

                while (
                    self.running
                    and
                    (
                        time.monotonic()
                        -
                        wait_start
                    )
                    <
                    MINIGAME_DETECTION_DELAY
                ):

                    
                    
                    
                    
                    
                    
                    

                    time.sleep(
                        0.05
                    )

                if not self.running:
                    break

                
                
                

                self.log(
                    "[INFO] Tempo de espera concluído."
                )

                self.log(
                    "[INFO] Agora procurando "
                    "o minigame..."
                )

                detected = (
                    self.wait_for_minigame()
                )

                
                
                

                if not detected:

                    if not self.running:
                        break

                    self.log(
                        "[AVISO] Minigame não apareceu."
                    )

                    self.log(
                        "[INFO] Tentando lançar "
                        "novamente..."
                    )

                    release_mouse()

                    reset_tracking()

                    time.sleep(
                        RETRY_DELAY
                    )

                    continue

                
                
                

                self.log(
                    "[OK] Minigame confirmado!"
                )

                self.status_signal.emit(
                    "FISHING"
                )

                
                
                

                self.fish()

                if not self.running:
                    break

                
                
                

                release_mouse()

                if WAIT_BEFORE_T_HOLD > 0:

                    self.log(
                        f"[INFO] Aguardando {WAIT_BEFORE_T_HOLD:.1f}"
                        "s antes de segurar T..."
                    )

                    wait_start = time.monotonic()

                    while (
                        self.running
                        and
                        (
                            time.monotonic()
                            -
                            wait_start
                        )
                        <
                        WAIT_BEFORE_T_HOLD
                    ):

                        time.sleep(0.05)

                    if not self.running:
                        break

                self.log(
                    "[INFO] Segurando T..."
                )

                self.status_signal.emit(
                    "T HOLD"
                )

                hold_t()

                if not self.running:
                    break

                self.log(
                    "[OK] T concluído"
                )

                reset_tracking()

                time.sleep(
                    RECAST_DELAY
                )

            except Exception as e:

                self.log(
                    f"[ERRO] {str(e)}"
                )

                release_mouse()

                reset_tracking()

                if self.running:

                    self.log(
                        "[AVISO] Erro recuperável. "
                        "Tentando novamente..."
                    )

                    time.sleep(
                        RETRY_DELAY
                    )

        cleanup()

        self.log(
            "[INFO] Bot parado"
        )

        self.status_signal.emit(
            "STOPPED"
        )

        self.running = False

    
    
    

    def wait_for_minigame(self):

        start_time = time.monotonic()

        stable_frames = 0

        delay = (
            1.0
            /
            FPS
        )

        while (
            self.running
            and
            (
                time.monotonic()
                -
                start_time
            )
            <
            CAST_TIMEOUT
        ):

            frame = capture()

            target = find_target(
                frame
            )

            player = find_player(
                frame
            )

            if (
                target is not None
                and
                player is not None
            ):

                stable_frames += 1

            else:

                stable_frames = 0

            
            
            

            if (
                stable_frames
                >=
                MINIGAME_CONFIRM_FRAMES
            ):

                return True

            time.sleep(
                delay
            )

        return False

    
    
    

    def fish(self):

        global lost_since

        delay = (
            1.0
            /
            FPS
        )

        reset_tracking()

        lost_since = None

        last_lost_log = 0

        while self.running:

            start = time.monotonic()

            frame = capture()

            target = find_target(
                frame
            )

            player = find_player(
                frame
            )

            
            
            

            if (
                target is not None
                and
                player is not None
            ):

                if lost_since is not None:

                    self.log(
                        "[OK] Minigame detectado novamente."
                    )

                lost_since = None

                _, target_y, _, _ = target

                _, player_y, _, _ = player

                update_velocity(
                    target_y,
                    player_y
                )

                (
                    action,
                    difference,
                    predicted_difference
                ) = control(
                    target_y,
                    player_y
                )

                log_msg = (
                    f"Alvo={target_y:3d} | "
                    f"Branco={player_y:3d} | "
                    f"Diff={difference:+4.0f} | "
                    f"Vel={player_velocity:+5.1f} | "
                    f"Pred={predicted_difference:+4.0f} | "
                    f"{action:7s} | "
                    f"{'DOWN' if mouse_held else 'UP  '}"
                )

                self.log(
                    log_msg
                )

                self.status_signal.emit(
                    f"FISHING | {action}"
                )

            
            
            

            else:

                release_mouse()

                if lost_since is None:

                    lost_since = (
                        time.monotonic()
                    )

                    last_lost_log = (
                        time.monotonic()
                    )

                    self.log(
                        "[AVISO] Minigame desapareceu..."
                    )

                lost_time = (
                    time.monotonic()
                    -
                    lost_since
                )

                self.status_signal.emit(
                    "LOST TARGET"
                )

                
                
                

                if (
                    not MINIMAL_LOGS
                    and
                    time.monotonic()
                    -
                    last_lost_log
                    >=
                    0.5
                ):

                    self.log(
                        f"[AVISO] Minigame desaparecido "
                        f"há {lost_time:.1f}s"
                    )

                    last_lost_log = (
                        time.monotonic()
                    )

                
                
                

                if (
                    lost_time
                    >=
                    LOST_TIMEOUT
                ):

                    self.log(
                        "[INFO] Minigame desapareceu "
                        "por tempo demais."
                    )

                    self.log(
                        "[INFO] Finalizando esta tentativa "
                        "e preparando novo lançamento..."
                    )

                    return False

            elapsed = (
                time.monotonic()
                -
                start
            )

            remaining = (
                delay
                -
                elapsed
            )

            if remaining > 0:

                time.sleep(
                    remaining
                )

        return False

    
    
    

    def stop(self):

        self.running = False

        release_mouse()






class SettingsDialog(QDialog):

    settings_changed = pyqtSignal()

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle(
            "⚙ Configurações"
        )

        self.setMinimumWidth(
            340
        )

        self.setStyleSheet("""
            QDialog {
                background-color: #0d1117;
            }

            QLabel {
                color: #c9d1d9;
            }

            QCheckBox {
                color: #c9d1d9;
                spacing: 8px;
            }

            QComboBox {
                background-color: #161b22;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 6px;
            }

            QComboBox QAbstractItemView {
                background-color: #161b22;
                color: #c9d1d9;
                border: 1px solid #30363d;
                selection-background-color: #4a9eff;
                selection-color: white;
                outline: none;
            }

            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                padding: 7px 14px;
                border-radius: 4px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #3d8ae8;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel(
            "⚙"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Bold
            )
        )

        layout.addWidget(
            title
        )

        
        
        

        language_layout = QHBoxLayout()

        language_label = QLabel("Idioma:")

        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Português",
            "English",
            "中文"
        ])
        self.language_combo.setCurrentIndex({"pt": 0, "en": 1, "zh": 2}.get(LANGUAGE, 0))

        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)

        layout.addLayout(language_layout)

        
        
        

        self.detailed_logs = QCheckBox(
            "Log Detalhado"
        )

        
        self.detailed_logs.setChecked(
            not MINIMAL_LOGS
        )

        layout.addWidget(
            self.detailed_logs
        )

        info = QLabel(
            "Mostra logs de cada frame. Desativado = logs minimalistas."
        )

        info.setStyleSheet(
            "color: #8b949e;"
        )

        info.setWordWrap(
            True
        )

        layout.addWidget(
            info
        )

        
        
        

        self.minimalist_mode = QCheckBox(
            "Minimalist Mode"
        )

        self.minimalist_mode.setChecked(
            MINIMALIST_MODE
        )

        layout.addWidget(
            self.minimalist_mode
        )

        
        
        

        color_layout = QHBoxLayout()

        color_label = QLabel(
            "Cor do programa:"
        )

        self.color_combo = QComboBox()

        self.color_combo.addItems(
            list(
                BACKGROUND_COLORS.keys()
            )
        )

        self.color_combo.setCurrentText(
            MINIMALIST_COLOR
        )

        color_layout.addWidget(
            color_label
        )

        color_layout.addWidget(
            self.color_combo
        )

        layout.addLayout(
            color_layout
        )

        info2 = QLabel(
            "No Minimalist Mode, a GIF/imagem "
            "de fundo fica desativada."
        )

        info2.setStyleSheet(
            "color: #8b949e;"
        )

        info2.setWordWrap(
            True
        )

        layout.addWidget(
            info2
        )

        
        
        

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok
            |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            self.apply_settings
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(
            buttons
        )

        self.setLayout(
            layout
        )

        mark_i18n_widgets(self)
        apply_i18n_widgets(self)

    def apply_settings(self):

        global MINIMAL_LOGS
        global MINIMALIST_MODE
        global MINIMALIST_COLOR
        global LANGUAGE

        LANGUAGE = ["pt", "en", "zh"][self.language_combo.currentIndex()]

        
        MINIMAL_LOGS = (
            not self.detailed_logs.isChecked()
        )

        MINIMALIST_MODE = (
            self.minimalist_mode.isChecked()
        )

        color_sources = [
            "Roxo escuro",
            "Preto",
            "Vermelho",
            "Azul",
            "Verde"
        ]

        MINIMALIST_COLOR = color_sources[
            self.color_combo.currentIndex()
        ]

        save_settings()
        self.settings_changed.emit()

        self.accept()






class FishingBotGUI(QMainWindow):

    hotkey_start_signal = pyqtSignal()
    hotkey_stop_signal = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.bot_thread = None

        self.bg_movie = None

        self.bg_label = None
        self.overlay_widget = None

        self.content_widget = None

        self.hotkey_handles = []

        self.init_ui()

        mark_i18n_widgets(self)
        apply_i18n_widgets(self)

        self.setup_hotkeys()

    
    
    

    def init_ui(self):

        self.setWindowTitle(
            "Slayer 2 Fishing by nilec2 & siegjf"
        )

        self.setGeometry(
            100,
            100,
            1000,
            700
        )

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        
        
        

        self.bg_label = QLabel(
            central_widget
        )

        self.bg_label.setScaledContents(
            True
        )

        self.bg_label.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )

        
        
        
        
        
        self.overlay_widget = QWidget(
            central_widget
        )

        self.overlay_widget.setStyleSheet(
            "background-color: rgba(0, 0, 0, 85);"
        )

        self.overlay_widget.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )

        self.overlay_widget.setGeometry(
            central_widget.rect()
        )

        self.setup_background()

        
        self.overlay_widget.raise_()

        
        
        

        self.content_widget = QWidget(
            central_widget
        )

        self.content_widget.setStyleSheet(
            "background: transparent;"
        )

        main_layout = QHBoxLayout(
            self.content_widget
        )

        main_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        left_panel = (
            self.create_control_panel()
        )

        right_panel = (
            self.create_log_panel()
        )

        main_layout.addLayout(
            left_panel,
            1
        )

        main_layout.addLayout(
            right_panel,
            2
        )

        self.content_widget.setGeometry(
            central_widget.rect()
        )

        
        
        self.overlay_widget.raise_()
        self.content_widget.raise_()

        
        
        

        self.settings_btn = QPushButton(
            "⚙",
            central_widget
        )

        self.settings_btn.setToolTip(
            "Configurações"
        )

        self.settings_btn.setFixedSize(
            42,
            42
        )

        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(13, 17, 23, 220);
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 21px;
                font-size: 20px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgba(74, 158, 255, 230);
                color: white;
            }
        """)

        self.settings_btn.clicked.connect(
            self.open_settings
        )

        self.settings_btn.raise_()

        
        
        
        self.apply_minimalist_styles()

    
    
    

    def setup_background(self):

        if MINIMALIST_MODE:

            self.stop_background()

            if self.overlay_widget:

                self.overlay_widget.hide()

            self.bg_label.setStyleSheet(
                "background-color: "
                +
                BACKGROUND_COLORS.get(
                    MINIMALIST_COLOR,
                    "#160022"
                )
            )

            self.bg_label.show()

            return

        gif_path = resource_path(
            "kurapika.gif"
        )

        
        
        

        if os.path.exists(
            gif_path
        ):

            self.stop_background()

            self.bg_movie = QMovie(
                gif_path
            )

            self.bg_movie.setCacheMode(
                QMovie.CacheAll
            )

            self.bg_label.setMovie(
                self.bg_movie
            )

            self.bg_movie.start()

            self.bg_label.setStyleSheet(
                "background-color: transparent;"
            )

            self.bg_label.show()

            if self.overlay_widget:

                self.overlay_widget.show()
                self.overlay_widget.raise_()

            if self.content_widget:

                self.content_widget.raise_()

            
            
            
            if hasattr(self, "settings_btn") and self.settings_btn:

                self.settings_btn.raise_()

            return

        
        
        

        self.stop_background()

        self.bg_label.setStyleSheet(
            "background-color: #1a1a1a;"
        )

        self.bg_label.show()

        if self.overlay_widget:

            self.overlay_widget.show()
            self.overlay_widget.raise_()

        if self.content_widget:

            self.content_widget.raise_()

        if hasattr(self, "settings_btn") and self.settings_btn:

            self.settings_btn.raise_()

    
    
    

    def stop_background(self):

        if self.bg_movie is not None:

            self.bg_movie.stop()

            self.bg_movie = None

        self.bg_label.clear()

    
    
    

    def open_settings(self):

        dialog = SettingsDialog(
            self
        )

        dialog.settings_changed.connect(
            self.apply_settings
        )

        dialog.exec_()

    def apply_settings(self):

        self.setup_background()

        self.apply_minimalist_styles()

        apply_i18n_widgets(self)

        
        if hasattr(self, "settings_btn") and self.settings_btn:

            self.settings_btn.raise_()

    
    
    

    def apply_minimalist_styles(self):

        if MINIMALIST_MODE:

            color = BACKGROUND_COLORS.get(
                MINIMALIST_COLOR,
                "#160022"
            )

            self.setStyleSheet(
                self.get_stylesheet(
                    color
                )
            )

        else:

            self.setStyleSheet(
                self.get_stylesheet(
                    None
                )
            )

        self.setup_background()

    def get_stylesheet(
        self,
        minimalist_color=None
    ):

        if minimalist_color:

            background = (
                minimalist_color
            )

        else:

            
            background = (
                "rgba(8, 8, 12, 215)"
            )

        return f"""

        QMainWindow {{
            background-color: transparent;
        }}

        QGroupBox {{
            color: #58a6ff;

            background-color: {background};

            border: 1px solid #30363d;

            border-radius: 6px;

            margin-top: 10px;

            padding-top: 10px;

            padding-left: 10px;

            padding-right: 10px;

            padding-bottom: 10px;

            font-weight: bold;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;

            left: 10px;

            padding:
                0 3px 0 3px;
        }}

        QLabel {{
            color: #c9d1d9;

            background-color: transparent;
        }}

        QComboBox {{
            background-color: rgba(22, 27, 34, 225);

            color: #c9d1d9;

            border: 1px solid #30363d;

            border-radius: 4px;

            padding: 6px;
        }}

        QSpinBox,
        QDoubleSpinBox {{
            background-color: #161b22;

            color: #c9d1d9;

            border: 1px solid #30363d;

            border-radius: 4px;

            padding: 6px;
        }}

        QComboBox:focus {{
            background-color: rgba(28, 33, 40, 235);

            border: 1px solid #58a6ff;
        }}

        QComboBox QAbstractItemView {{
            background-color: #161b22;
            color: #c9d1d9;
            border: 1px solid #30363d;
            selection-background-color: #4a9eff;
            selection-color: white;
            outline: none;
        }}

        QComboBox QAbstractItemView::item {{
            padding: 6px;
        }}

        QSpinBox:focus,
        QDoubleSpinBox:focus {{
            background-color: #1c2128;

            border: 1px solid #58a6ff;
        }}

        QTextEdit {{
            background-color: rgba(10, 10, 10, 190);

            color: #c9d1d9;

            border: 1px solid #30363d;

            border-radius: 5px;
        }}

        QPushButton {{
            border: none;

            font-weight: bold;

            font-size: 11px;

            color: white;
        }}

        QPushButton:disabled {{
            background-color: #30363d !important;

            color: #8b949e !important;
        }}

        """

    
    
    

    def create_control_panel(self):

        layout = QVBoxLayout()

        
        
        

        status_group = QGroupBox(
            "Status"
        )

        status_layout = QVBoxLayout()

        self.status_label = QLabel(
            "PARADO"
        )

        self.status_label.setFont(
            QFont(
                "Consolas",
                14,
                QFont.Bold
            )
        )

        self.status_label.setStyleSheet(
            "color: #ff6b6b;"
            "background-color: #1a1a1a;"
            "padding: 10px;"
            "border-radius: 5px;"
        )

        status_layout.addWidget(
            self.status_label
        )

        status_group.setLayout(
            status_layout
        )

        layout.addWidget(
            status_group
        )

        
        
        

        hotkey_group = QGroupBox(
            "Hotkeys"
        )

        hotkey_layout = QGridLayout()

        hotkey_layout.addWidget(
            QLabel("Iniciar:"),
            0,
            0
        )

        self.start_hotkey = QComboBox()

        self.start_hotkey.addItems(
            [
                "f8",
                "f7",
                "f6",
                "f5",
                "f4"
            ]
        )

        self.start_hotkey.setCurrentText(
            "f8"
        )

        hotkey_layout.addWidget(
            self.start_hotkey,
            0,
            1
        )

        hotkey_layout.addWidget(
            QLabel("Parar:"),
            1,
            0
        )

        self.stop_hotkey = QComboBox()

        self.stop_hotkey.addItems(
            [
                "f9",
                "f10",
                "f11",
                "esc"
            ]
        )

        self.stop_hotkey.setCurrentText(
            "f9"
        )

        hotkey_layout.addWidget(
            self.stop_hotkey,
            1,
            1
        )

        hotkey_layout.addWidget(
            QLabel("Extras:"),
            2,
            0
        )

        hotkey_layout.addWidget(
            QLabel(
                "Ctrl+C / Esc"
            ),
            2,
            1
        )

        hotkey_group.setLayout(
            hotkey_layout
        )

        layout.addWidget(
            hotkey_group
        )

        
        
        

        button_layout = QHBoxLayout()

        self.select_region_btn = QPushButton(
            "Selecionar Região"
        )

        self.select_region_btn.clicked.connect(
            self.select_region
        )

        self.select_region_btn.setStyleSheet(
            "background-color: #4a9eff;"
            "color: white;"
            "padding: 8px;"
            "border-radius: 5px;"
        )

        button_layout.addWidget(
            self.select_region_btn
        )

        self.start_btn = QPushButton(
            "▶ Iniciar"
        )

        self.start_btn.clicked.connect(
            self.start_bot
        )

        self.start_btn.setStyleSheet(
            "background-color: #51cf66;"
            "color: white;"
            "padding: 8px;"
            "border-radius: 5px;"
        )

        button_layout.addWidget(
            self.start_btn
        )

        self.stop_btn = QPushButton(
            "Parar"
        )

        self.stop_btn.clicked.connect(
            self.stop_bot
        )

        self.stop_btn.setStyleSheet(
            "background-color: #ff6b6b;"
            "color: white;"
            "padding: 8px;"
            "border-radius: 5px;"
        )

        self.stop_btn.setEnabled(
            False
        )

        button_layout.addWidget(
            self.stop_btn
        )

        layout.addLayout(
            button_layout
        )

        
        
        

        stats_group = QGroupBox(
            "Configurações"
        )

        stats_layout = QGridLayout()

        stats_layout.addWidget(
            QLabel("FPS:"),
            0,
            0
        )

        self.fps_spinbox = QSpinBox()

        self.fps_spinbox.setValue(
            FPS
        )

        self.fps_spinbox.setRange(
            10,
            60
        )

        stats_layout.addWidget(
            self.fps_spinbox,
            0,
            1
        )

        stats_layout.addWidget(
            QLabel("Deadzone:"),
            1,
            0
        )

        self.deadzone_spinbox = QSpinBox()

        self.deadzone_spinbox.setValue(
            DEADZONE
        )

        self.deadzone_spinbox.setRange(
            1,
            20
        )

        stats_layout.addWidget(
            self.deadzone_spinbox,
            1,
            1
        )

        stats_layout.addWidget(
            QLabel("Brake Zone:"),
            2,
            0
        )

        self.brake_spinbox = QSpinBox()

        self.brake_spinbox.setValue(
            BRAKE_ZONE
        )

        self.brake_spinbox.setRange(
            1,
            50
        )

        stats_layout.addWidget(
            self.brake_spinbox,
            2,
            1
        )

        stats_layout.addWidget(
            QLabel("Prediction:"),
            3,
            0
        )

        self.prediction_spinbox = (
            QDoubleSpinBox()
        )

        self.prediction_spinbox.setValue(
            PREDICTION
        )

        self.prediction_spinbox.setRange(
            0.0,
            1.0
        )

        self.prediction_spinbox.setSingleStep(
            0.05
        )

        stats_layout.addWidget(
            self.prediction_spinbox,
            3,
            1
        )

        stats_layout.addWidget(
            QLabel("Cast Timeout (s):"),
            4,
            0
        )

        self.cast_timeout_spinbox = QSpinBox()

        self.cast_timeout_spinbox.setValue(
            CAST_TIMEOUT
        )

        self.cast_timeout_spinbox.setRange(
            1,
            30
        )

        self.cast_timeout_spinbox.setToolTip(
            "Tempo máximo procurando o minigame após lançamento"
        )

        stats_layout.addWidget(
            self.cast_timeout_spinbox,
            4,
            1
        )

        stats_layout.addWidget(
            QLabel("Espera Detectar (s):"),
            5,
            0
        )

        self.detection_delay_spinbox = QSpinBox()

        self.detection_delay_spinbox.setValue(
            MINIGAME_DETECTION_DELAY
        )

        self.detection_delay_spinbox.setRange(
            1,
            30
        )

        self.detection_delay_spinbox.setToolTip(
            "Tempo que aguarda antes de detectar o minigame"
        )

        stats_layout.addWidget(
            self.detection_delay_spinbox,
            5,
            1
        )

        stats_layout.addWidget(
            QLabel("Espera T (s):"),
            6,
            0
        )

        self.wait_t_spinbox = QDoubleSpinBox()

        self.wait_t_spinbox.setValue(
            WAIT_BEFORE_T_HOLD
        )

        self.wait_t_spinbox.setRange(
            0.0,
            30.0
        )

        self.wait_t_spinbox.setSingleStep(
            0.1
        )

        self.wait_t_spinbox.setDecimals(
            1
        )

        self.wait_t_spinbox.setToolTip(
            "Tempo que aguarda antes de segurar T"
        )

        stats_layout.addWidget(
            self.wait_t_spinbox,
            6,
            1
        )

        stats_group.setLayout(
            stats_layout
        )

        layout.addWidget(
            stats_group
        )

        
        
        

        clear_btn = QPushButton(
            "🗑 Limpar Logs"
        )

        clear_btn.clicked.connect(
            self.clear_logs
        )

        clear_btn.setStyleSheet(
            "background-color: #868e96;"
            "color: white;"
            "padding: 8px;"
            "border-radius: 5px;"
        )

        layout.addWidget(
            clear_btn
        )

        layout.addStretch()

        return layout

    
    
    

    def create_log_panel(self):

        layout = QVBoxLayout()

        title = QLabel(
            "Logs"
        )

        title.setFont(
            QFont(
                "Consolas",
                12,
                QFont.Bold
            )
        )

        title.setStyleSheet(
            "color: #4a9eff;"
        )

        layout.addWidget(
            title
        )

        self.log_text = QTextEdit()

        self.log_text.setReadOnly(
            True
        )

        self.log_text.setFont(
            QFont(
                "Consolas",
                9
            )
        )

        
        
        
        self.log_text.document().setMaximumBlockCount(
            3000
        )

        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(13, 17, 23, 210);
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 5px;
            }
        """)

        layout.addWidget(
            self.log_text
        )

        return layout

    
    
    

    def select_region(self):

        global GEOMETRY

        import tkinter as tk

        self.log_text.append(
            translate_runtime_text("[INFO] Selecione a região...")
        )

        selection = {
            "x1": None,
            "y1": None,
            "x2": None,
            "y2": None
        }

        selecting = {
            "active": False
        }

        root = tk.Tk()

        root.attributes(
            "-fullscreen",
            True
        )

        root.attributes(
            "-topmost",
            True
        )

        root.configure(
            bg="black"
        )

        root.attributes(
            "-alpha",
            0.25
        )

        canvas = tk.Canvas(
            root,
            cursor="cross",
            bg="black",
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True
        )

        rectangle = None

        def mouse_down(event):

            nonlocal rectangle

            selection["x1"] = event.x
            selection["y1"] = event.y

            selection["x2"] = event.x
            selection["y2"] = event.y

            selecting["active"] = True

            if rectangle is not None:

                canvas.delete(
                    rectangle
                )

            rectangle = canvas.create_rectangle(
                event.x,
                event.y,
                event.x,
                event.y,
                outline="red",
                width=2
            )

        def mouse_move(event):

            nonlocal rectangle

            if not selecting["active"]:
                return

            selection["x2"] = event.x
            selection["y2"] = event.y

            if rectangle is not None:

                canvas.coords(
                    rectangle,
                    selection["x1"],
                    selection["y1"],
                    selection["x2"],
                    selection["y2"]
                )

        def mouse_up(event):

            selection["x2"] = event.x
            selection["y2"] = event.y

            selecting["active"] = False

        def confirm(event=None):

            if all(
                v is not None
                for v in selection.values()
            ):

                root.quit()

        def cancel(event=None):

            selection["x1"] = None

            root.quit()

        canvas.bind(
            "<ButtonPress-1>",
            mouse_down
        )

        canvas.bind(
            "<B1-Motion>",
            mouse_move
        )

        canvas.bind(
            "<ButtonRelease-1>",
            mouse_up
        )

        root.bind(
            "<Return>",
            confirm
        )

        root.bind(
            "<Escape>",
            cancel
        )

        root.mainloop()

        root.destroy()

        if selection["x1"] is None:

            self.log_text.append(
                translate_runtime_text("[ERRO] Seleção cancelada")
            )

            return

        x1 = min(
            selection["x1"],
            selection["x2"]
        )

        y1 = min(
            selection["y1"],
            selection["y2"]
        )

        x2 = max(
            selection["x1"],
            selection["x2"]
        )

        y2 = max(
            selection["y1"],
            selection["y2"]
        )

        width = x2 - x1
        height = y2 - y1

        if (
            width <= 0
            or
            height <= 0
        ):

            self.log_text.append(
                translate_runtime_text("[ERRO] Região inválida")
            )

            return

        GEOMETRY = {
            "left": x1,
            "top": y1,
            "width": width,
            "height": height
        }

        self.log_text.append(
            translate_runtime_text(
                f"[OK] Região selecionada: {GEOMETRY}"
            )
        )

    
    
    

    def start_bot(self):

        global FPS
        global DEADZONE
        global BRAKE_ZONE
        global PREDICTION
        global CAST_TIMEOUT
        global MINIGAME_DETECTION_DELAY
        global WAIT_BEFORE_T_HOLD

        if (
            self.bot_thread
            and
            self.bot_thread.running
        ):

            return

        if GEOMETRY is None:

            QMessageBox.warning(
                self,
                tr("Aviso"),
                tr("Selecione a região primeiro!")
            )

            return

        FPS = (
            self.fps_spinbox.value()
        )

        DEADZONE = (
            self.deadzone_spinbox.value()
        )

        BRAKE_ZONE = (
            self.brake_spinbox.value()
        )

        PREDICTION = (
            self.prediction_spinbox.value()
        )

        CAST_TIMEOUT = (
            self.cast_timeout_spinbox.value()
        )

        MINIGAME_DETECTION_DELAY = (
            self.detection_delay_spinbox.value()
        )

        WAIT_BEFORE_T_HOLD = (
            self.wait_t_spinbox.value()
        )

        save_settings()

        self.bot_thread = BotThread()

        self.bot_thread.log_signal.connect(
            self.add_log
        )

        self.bot_thread.status_signal.connect(
            self.update_status
        )

        self.bot_thread.start()

        self.start_btn.setEnabled(
            False
        )

        self.stop_btn.setEnabled(
            True
        )

        self.select_region_btn.setEnabled(
            False
        )

        self.log_text.append(
            "[INFO] Bot iniciado em "
            +
            datetime.now().strftime(
                "%H:%M:%S"
            )
        )

    
    
    

    def stop_bot(self):

        if (
            self.bot_thread
            and
            self.bot_thread.running
        ):

            self.bot_thread.stop()

            self.bot_thread.wait(
                3000
            )

        cleanup()

        self.start_btn.setEnabled(
            True
        )

        self.stop_btn.setEnabled(
            False
        )

        self.select_region_btn.setEnabled(
            True
        )

        self.update_status(
            "PARADO"
        )

    
    
    

    def add_log(
        self,
        message
    ):

        self.log_text.append(
            message
        )

        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    
    
    

    def update_status(
        self,
        status
    ):

        status_colors = {

            "PARADO":
                "#ff6b6b",

            "FISHING":
                "#51cf66",

            "T HOLD":
                "#ffd93d",

            "LOST TARGET":
                "#ff922b",

            "STOPPED":
                "#ff6b6b",

            "AGUARDANDO MINIGAME":
                "#ffd93d"
        }

        base_status = (
            status.split(
                " | "
            )[0]
        )

        if base_status.startswith(
            "CAST #"
        ):

            color = "#4a9eff"

        else:

            color = status_colors.get(
                base_status,
                "#858585"
            )

        self.status_label.setText(
            translate_runtime_text(status)
        )

        self.status_label.setStyleSheet(
            f"""
            color: {color};

            background-color: #1a1a1a;

            padding: 10px;

            border-radius: 5px;
            """
        )

    
    
    

    def clear_logs(self):

        self.log_text.clear()

        self.log_text.append(
            "[INFO] Logs limpos"
        )

    
    
    

    def setup_hotkeys(self):

        self.hotkey_start_signal.connect(
            self.start_bot
        )

        self.hotkey_stop_signal.connect(
            self.stop_bot
        )

        
        self.hotkey_handles.append(
            keyboard.add_hotkey(
                "f8",
                lambda:
                self.hotkey_start_signal.emit()
            )
        )

        
        self.hotkey_handles.append(
            keyboard.add_hotkey(
                "f9",
                lambda:
                self.hotkey_stop_signal.emit()
            )
        )

        
        self.hotkey_handles.append(
            keyboard.add_hotkey(
                "esc",
                lambda:
                self.hotkey_stop_signal.emit()
            )
        )

        
        self.hotkey_handles.append(
            keyboard.add_hotkey(
                "ctrl+c",
                lambda:
                self.hotkey_stop_signal.emit()
            )
        )

        
        self.hotkey_handles.append(
            keyboard.add_hotkey(
                "ctrl+f8",
                lambda:
                self.hotkey_start_signal.emit()
            )
        )

        
        self.hotkey_handles.append(
            keyboard.add_hotkey(
                "ctrl+f9",
                lambda:
                self.hotkey_stop_signal.emit()
            )
        )

    
    
    

    def resizeEvent(
        self,
        event
    ):

        super().resizeEvent(
            event
        )

        if self.centralWidget():

            rect = (
                self.centralWidget().rect()
            )

            if self.bg_label:

                self.bg_label.setGeometry(
                    rect
                )

            if self.overlay_widget:

                self.overlay_widget.setGeometry(
                    rect
                )
                self.overlay_widget.lower()
                self.overlay_widget.raise_()

            if self.content_widget:

                self.content_widget.setGeometry(
                    rect
                )
                self.content_widget.raise_()

            if self.settings_btn:

                self.settings_btn.move(
                    rect.width()
                    -
                    self.settings_btn.width()
                    -
                    15,

                    15
                )

                self.settings_btn.raise_()

    
    
    

    def closeEvent(
        self,
        event
    ):

        global FPS
        global DEADZONE
        global BRAKE_ZONE
        global PREDICTION
        global CAST_TIMEOUT
        global MINIGAME_DETECTION_DELAY
        global WAIT_BEFORE_T_HOLD

        try:
            FPS = self.fps_spinbox.value()
            DEADZONE = self.deadzone_spinbox.value()
            BRAKE_ZONE = self.brake_spinbox.value()
            PREDICTION = self.prediction_spinbox.value()
            CAST_TIMEOUT = self.cast_timeout_spinbox.value()
            MINIGAME_DETECTION_DELAY = self.detection_delay_spinbox.value()
            WAIT_BEFORE_T_HOLD = self.wait_t_spinbox.value()
            save_settings()
        except Exception:
            pass

        try:

            for handle in (
                self.hotkey_handles
            ):

                keyboard.remove_hotkey(
                    handle
                )

        except Exception:
            pass

        self.stop_bot()

        self.stop_background()

        event.accept()






def signal_handler(
    sig,
    frame
):

    cleanup()

    sys.exit(
        0
    )


signal.signal(
    signal.SIGINT,
    signal_handler
)

signal.signal(
    signal.SIGTERM,
    signal_handler
)






if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    
    app.setWindowIcon(
        QIcon(
            resource_path("giyuu.ico")
        )
    )

    window = FishingBotGUI()

    
    window.setWindowIcon(
        QIcon(
            resource_path("giyuu.ico")
        )
    )

    window.show()

    sys.exit(
        app.exec_()
    )
