# -*- coding: gb2312 -*-
__author__ = 'WangYi'
__version__ = 0.1

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from gui import Ui_Form

import time
import math


class Test(QWidget, Ui_Form):
    def __init__(self):
        super(Test, self).__init__()
        self.setupUi(self)

    def on_btn_xor_clicked(self):  # 求累加和函数 槽函数的实现 形参需要self 信号连接槽由qt designer自动完成
        tmp = list()
        tmp.append(self.spinBox_4.value())
        tmp.append(self.spinBox_5.value())
        tmp.append(self.spinBox_6.value())
        tmp.append(self.spinBox_7.value())
        tmp.append(self.spinBox_8.value())
        tmp.append(self.spinBox_9.value())

        res = 0
        for i in tmp:
            res = res ^ i

        self.spinBox_10.setValue(res)

    def on_btn_cmd_fout_clicked(self):  # 槽函数 文件输出函数
        self.on_btn_xor_clicked()  # 先求累加和 再保存数据
        tmp = list()
        tmp.append(self.spinBox_1.value())
        tmp.append(self.spinBox_2.value())
        tmp.append(self.spinBox_3.value())
        tmp.append(self.spinBox_4.value())
        tmp.append(self.spinBox_5.value())
        tmp.append(self.spinBox_6.value())
        tmp.append(self.spinBox_7.value())
        tmp.append(self.spinBox_8.value())
        tmp.append(self.spinBox_9.value())
        tmp.append(self.spinBox_10.value())

        wr_dat = list()
        for i in tmp:  # 转换为字符型
            j = hex(i)
            j = j[2:]  # 去除0x
            wr_dat.append(j.zfill(4))

        outfmt = '(卫星格式)'
        if not self.radioButton_1.isChecked():  # 如果选择地检输出 需要补齐256字节
            for i in range(0, 128 - len(wr_dat)):
                wr_dat.append('AAAA')
            outfmt = '( 地检格式)'
        else:
            outfmt = '( 卫星格式)'

        filename = self.lineEdit_cmd_filename.text() + '.txt'
        f = open(filename, mode='w')
        for i in wr_dat:
            f.write(i)
        f.close()

        #  日志输出字符串准备
        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        txt_out = now + '输出文件' + filename + outfmt
        self.textBrowser_log.append(txt_out)

    def on_btn_odu_gain_update(self):
        gain = self.doubleSpinBox_odu_gain.value()  # 获取增益物理量
        G = 76.125 - 76.125/gain
        self.spinBox_odu_gain_hex.setValue(int(G))
        self.spinBox_5.setValue(0x0f02)
        self.spinBox_6.setValue(0x2000 | int(G))
        self.spinBox_9.setValue(0x0102)

    def on_radio_dpc_cmdfmt(self):   # 数据注入格式
        self.spinBox_4.setValue(0x0a)

    def on_radio_dpc_yzfmt(self):  # 载荷工作包格式
        self.spinBox_4.setValue(0x0004)

    def on_btn_odu_time_update_1(self):   # 积分时间1修改
        i_time = self.doubleSpinBox_odu_time.value()  # 获取积分时间物理量
        i_time_hex = int(i_time * 2)
        self.spinBox_odu_time_hex.setValue(i_time_hex)
        self.spinBox_5.setValue(0x0f05)
        tmp1 = (i_time_hex << 8) & 0xff00
        tmp2 = tmp1 | i_time_hex
        self.spinBox_6.setValue(tmp2)
        self.spinBox_7.setValue(tmp2)
        tmp2 = tmp1 | 0xeb
        self.spinBox_8.setValue(tmp2)
        self.spinBox_9.setValue(0x0105)

    def on_btn_odu_time_update_2(self):   # 积分时间2修改
        i_time = self.doubleSpinBox_odu_time.value()  # 获取积分时间物理量
        i_time_hex = int(i_time * 2)
        self.spinBox_odu_time_hex.setValue(i_time_hex)
        self.spinBox_5.setValue(0x0f06)
        tmp1 = (i_time_hex << 8) & 0xff00
        tmp2 = tmp1 | i_time_hex
        self.spinBox_6.setValue(tmp2)
        self.spinBox_7.setValue(tmp2)
        tmp2 = tmp1 | 0xeb
        self.spinBox_8.setValue(tmp2)
        self.spinBox_9.setValue(0x0106)

    def on_btn_odu_time_update_3(self):   # 积分时间3修改
        i_time = self.doubleSpinBox_odu_time.value()  # 获取积分时间物理量
        i_time_hex = int(i_time * 2)
        self.spinBox_odu_time_hex.setValue(i_time_hex)
        self.spinBox_5.setValue(0x0f07)
        tmp1 = (i_time_hex << 8) & 0xff00
        tmp2 = tmp1 | i_time_hex
        self.spinBox_6.setValue(tmp2)
        self.spinBox_7.setValue(tmp2)
        tmp2 = tmp1 | 0xeb
        self.spinBox_8.setValue(tmp2)
        self.spinBox_9.setValue(0x0107)

    def on_btn_djmode_clicked(self):  # 电机工作模式更新
        # 获取电机模式
        tmp = self.comboBox_djmode.currentIndex()
        if tmp == 0:
            djmode = 0xaa
        elif tmp == 1:
            djmode = 0xbb
        else:
            djmode = 0xee

        # 获取脉冲发送模式
        tmp = self.comboBox_djpulse.currentIndex()
        if tmp == 0:
            djpulse = 0x10
        else:
            djpulse = 0x20

        # 获取获取功率模式
        tmp = self.comboBox_djpower.currentIndex()
        if tmp == 0:
            djpower = 0x11
        else:
            djpower = 0x22

        # 获取获取斩波频率
        tmp = self.comboBox_djfreq.currentIndex()
        if tmp == 0:  # 20k
            djfreq_H = 0x02
            djfreq_L = 0x29EB
        else:   # 20k
            djfreq_H = 0x01
            djfreq_L = 0x14eb

        # 高低字节拼接
        apdata2 = ((djmode << 8) & 0xff00) | djpulse
        apdata3 = ((djpower << 8) & 0xff00) | djfreq_H
        apdata4 = djfreq_L

        # 更新数值
        self.spinBox_5.setValue(0xcc37)
        self.spinBox_6.setValue(apdata2)
        self.spinBox_7.setValue(apdata3)
        self.spinBox_8.setValue(apdata4)
        self.spinBox_9.setValue(0x1107)

    def on_btn_djrpm_clicked(self):  # 电机转速设置
        self.spinBox_5.setValue(0xcc38)
        self.spinBox_6.setValue(self.spinBox_dj_start_rpm.value())
        self.spinBox_7.setValue(self.spinBox_dj_work_rpm.value())
        self.spinBox_8.setValue(0xebeb)
        self.spinBox_9.setValue(0x1108)

    def on_btn_djrelay_clicked(self):  # 延时时间设置
        self.spinBox_5.setValue(0xcc39)
        self.spinBox_6.setValue(self.spinBox_dj_relay.value())
        self.spinBox_7.setValue(0xebeb)
        self.spinBox_8.setValue(0xebeb)
        self.spinBox_9.setValue(0x1109)

    def on_btn_djpos_clicked(self):  # 圈帧同步脉冲发送位置设置
        apdata = ((self.spinBox_dj_loop_width.value() << 8) & 0xff00) | 0xeb

        self.spinBox_5.setValue(0xcc3a)
        self.spinBox_6.setValue(self.spinBox_dj_loop_pos.value())
        self.spinBox_7.setValue(self.spinBox_dj_frame_pos.value())
        self.spinBox_8.setValue(apdata)
        self.spinBox_9.setValue(0x110a)


    def on_radio_sel_mf501(self):  # 按钮选择mf501
        self.doubleSpinBox_rta.setValue(-6.011)
        self.doubleSpinBox_rtb.setValue(4622.533)
        self.doubleSpinBox_rtc.setValue(-86421.724)


    def on_radio_sel_mf61(self):  # 按钮选择mf61
        self.doubleSpinBox_rta.setValue(-4.362)
        self.doubleSpinBox_rtb.setValue(4081.702)
        self.doubleSpinBox_rtc.setValue(-94033.780)


    # 温度值转DN值 内部函数
    def t2dn(self, temperature, resup=10000 , maxdn=4095):
        t = temperature + 273.15

        a = self.doubleSpinBox_rta.value()
        b = self.doubleSpinBox_rtb.value()
        c = self.doubleSpinBox_rtc.value()

        rt = math.exp(a + b / t + c / (t * t))

        dn = maxdn * rt / (rt + resup)

        return int(dn)

    # 温度值转DN值 内部函数
    def dn2t(self, dn, resup=10000, maxdn=4095):

        a = self.doubleSpinBox_rta.value()
        b = self.doubleSpinBox_rtb.value()
        c = self.doubleSpinBox_rtc.value()

        rt = math.log(resup*dn/(maxdn-dn))

        t = -273.15 + 2*c/(-b + math.sqrt(b*b - 4*c*(a - rt)))

        return t

    def on_btn_wk_t2dn_clicked(self):  # 温度转DN
        resup = self.spinBox_wk_res_up.value()
        dnmax = self.spinBox_wk_dnmax.value()

        t = self.doubleSpinBox_temperautre_t.value()
        dn = self.t2dn(t, resup, dnmax)

        self.spinBox_temperautre_dn.setValue(dn)

    def on_btn_wk_dn2t_clicked(self):  # DN转温度
        resup = self.spinBox_wk_res_up.value()
        dnmax = self.spinBox_wk_dnmax.value()

        dn = self.spinBox_temperautre_dn.value()

        t = self.dn2t(dn, resup, dnmax)

        self.doubleSpinBox_temperautre_t.setValue(t)

    def on_btn_dpcmode_clicked(self):  # 修改工作模式
        mode_index = self.comboBox_dpcmode_1.currentIndex()
        sheet_index = self.comboBox_dpcmode_2.currentIndex()

        if mode_index == 0:
            mode = 0x11
        elif mode_index == 1:
            mode = 0x22
        else:
            mode = 0x33

        if sheet_index == 0:
            sheet = 0x0e
        elif sheet_index == 1:
            sheet = 0x0f
        elif sheet_index == 2:
            sheet = 0x0d
        else:
            sheet = 0xeb

        apdata = ((mode << 8) & 0xff00) | sheet

        self.spinBox_5.setValue(0x1103)
        self.spinBox_6.setValue(apdata)
        self.spinBox_7.setValue(0xebeb)
        self.spinBox_8.setValue(0xebeb)
        self.spinBox_9.setValue(0xffff)


    def on_btn_orbit_clicked(self):  # 修改轨道序号
        self.spinBox_5.setValue(0x1106)
        self.spinBox_6.setValue(0xebeb)
        self.spinBox_7.setValue(0xebeb)
        self.spinBox_8.setValue(self.spinBox_orbit.value())
        self.spinBox_9.setValue(0xffff)

    def on_btn_orbit_time_clicked(self): # 计算轨道周期
        orbit_time = self.doubleSpinBox_orbittime.value()
        orbit_time_dn = orbit_time*60*1000/0.1
        self.spinBox_orbittime_dn.setValue(int(orbit_time_dn))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = Test()
    mywidget.show()
    sys.exit(app.exec_())
