# -*- coding: UTF-8 -*-
__author__ = 'WangYi'
__version__ = 0.1

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from gui import Ui_Form
from PyQt5.QtWidgets import QMessageBox

import time
import math


class Test(QWidget, Ui_Form):
    def __init__(self):
        super(Test, self).__init__()
        self.setupUi(self)

    def on_btn_xor_clicked(self):  # 求累加和函数 槽函数的实现 形参需要self 信号连接槽由qt designer自动完成
        tmp = list()

        # 第一部分 高五大气数据注入的累加和
        if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五格式
            tmp.append(self.spinBox_1.value())
            tmp.append(self.spinBox_2.value())
            tmp.append(self.spinBox_3.value())
        else:
            pass

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

        # 第二部分 高五延时注数的累加和
        foo = list()
        foo.append(self.spinBox_yz_1.value())
        foo.append(self.spinBox_yz_2.value())
        foo.append(self.spinBox_yz_3.value())
        foo.append(self.spinBox_yz_4.value())
        foo.append(self.spinBox_yz_5.value())
        foo.append(self.spinBox_yz_6.value())

        res = 0
        for i in foo:
            res = res ^ i
        
        self.spinBox_yz_7.setValue(res)


    def on_btn_cmd_fout_clicked(self):  # 槽函数 数据注入文件输出函数        
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

        cmd_code = "".join(wr_dat)  # 字符串拼接 用于显示
        
        outfmt = '(卫星格式)'
        if not self.radioButton_1.isChecked():  # 如果选择地检输出 需要补齐256字节
            if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五格式 需要128字节
                for i in range(0, 32 - len(wr_dat)):
                    wr_dat.append('AAAA')
            else:  # 选择大气格式需要补齐256字节
                for i in range(0, 128 - len(wr_dat)):
                    wr_dat.append('AAAA')
            outfmt = '( 地检格式)'
        else:
            outfmt = '( 卫星格式)'

        filename = self.lineEdit_cmd_filename.text() + '.txt'
        # 文件头加标识 证明是DQ还是GF
        if self.radioButton_gfdpc_yzfmt.isChecked() :
            filename = 'GF-' + filename
        else:
            filename = 'DQ-' + filename
        
        f = open(filename, mode='w')
        for i in wr_dat:
            f.write(i)
        f.close()

        # 日志输出字符串准备
        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        txt_out = now + '数据注入输出文件:' + filename + outfmt
        self.textBrowser_log.append(txt_out)        
        self.textBrowser_log.append("指令码为: " + cmd_code)


    def on_btn_cmd_g5yz_fout_clicked(self):  # 高五延时注数文件
        self.on_btn_xor_clicked()  # 先求累加和 再保存数据
        tmp = list()
        tmp.append(self.spinBox_yz_1.value())
        tmp.append(self.spinBox_yz_2.value())
        tmp.append(self.spinBox_yz_3.value())
        tmp.append(self.spinBox_yz_4.value())
        tmp.append(self.spinBox_yz_5.value())
        tmp.append(self.spinBox_yz_6.value())
        tmp.append(self.spinBox_yz_7.value())
        tmp.append(self.spinBox_yz_8.value())
        tmp.append(self.spinBox_yz_9.value())        

        wr_dat = list()
        for i in tmp:  # 转换为字符型
            j = hex(i)
            j = j[2:]  # 去除0x
            wr_dat.append(j.zfill(4))

        # 文件输出
        filename = 'GF-YZ-' + self.lineEdit_cmd_filename.text() + '.txt'
        f = open(filename, mode='w')
        for i in wr_dat:
            f.write(i)
        f.close()

        # 日志输出字符串准备
        now = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
        txt_out = now + '高五延时注入输出文件:' + filename
        self.textBrowser_log.append(txt_out)
    

    def on_btn_odu_gain_update(self):
        gain = self.doubleSpinBox_odu_gain.value()  # 获取增益物理量
        G = 76.125 - 76.125/gain
        self.spinBox_odu_gain_hex.setValue(int(G))
        # 数据注入
        self.spinBox_5.setValue(0x0f02)
        self.spinBox_6.setValue(0x2000 | int(G))
        if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五注数格式
            self.spinBox_9.setValue(0x0502)
        else:
            self.spinBox_9.setValue(0x0102)
        
        # 高五延时注数
        self.spinBox_yz_2.setValue(0x0f02)
        self.spinBox_yz_3.setValue(0x2000 | int(G)) 
        self.spinBox_yz_4.setValue(0xebeb)
        self.spinBox_yz_5.setValue(0xebeb)
        self.spinBox_yz_6.setValue(0x0502)

        self.on_btn_xor_clicked()  # 自动求累加和



    def on_radio_dpc_cmdfmt(self):   # 数据注入格式
        self.spinBox_4.setValue(0x0a)
        self.spinBox_1.setValue(0x1690)

    def on_radio_dpc_yzfmt(self):  # 载荷工作包格式
        self.spinBox_4.setValue(0x0004)
        self.spinBox_1.setValue(0x1690)

    def on_radio_gfdpc_yzfmt(self):  # 选择高五注数格式
        self.spinBox_1.setValue(0x1637)
        self.spinBox_4.setValue(0x000a)

    def on_btn_odu_time_update_1(self):   # 积分时间1修改
        i_time = self.doubleSpinBox_odu_time.value()  # 获取积分时间物理量
        i_time_hex = int(i_time * 2)
        self.spinBox_odu_time_hex.setValue(i_time_hex)

        self.spinBox_5.setValue(0x0f05)
        self.spinBox_yz_2.setValue(0x0f05)  # 延时注数

        tmp1 = (i_time_hex << 8) & 0xff00
        tmp2 = tmp1 | i_time_hex
        self.spinBox_6.setValue(tmp2)
        self.spinBox_7.setValue(tmp2)
        self.spinBox_yz_3.setValue(tmp2)
        self.spinBox_yz_4.setValue(tmp2)

        tmp2 = tmp1 | 0xeb
        self.spinBox_8.setValue(tmp2)
        self.spinBox_yz_5.setValue(tmp2)

        if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五格式
            self.spinBox_9.setValue(0x0505)
        else:
            self.spinBox_9.setValue(0x0105)
        
        self.spinBox_yz_6.setValue(0x0505)  # 延时
        self.on_btn_xor_clicked()  # 自动求累加和



    def on_btn_odu_time_update_2(self):   # 积分时间2修改
        i_time = self.doubleSpinBox_odu_time.value()  # 
        i_time_hex = int(i_time * 2)
        self.spinBox_odu_time_hex.setValue(i_time_hex)
        self.spinBox_5.setValue(0x0f06)
        self.spinBox_yz_2.setValue(0x0f06)  # 延时注数

        tmp1 = (i_time_hex << 8) & 0xff00
        tmp2 = tmp1 | i_time_hex
        self.spinBox_6.setValue(tmp2)
        self.spinBox_7.setValue(tmp2)
        self.spinBox_yz_3.setValue(tmp2)
        self.spinBox_yz_4.setValue(tmp2)

        tmp2 = tmp1 | 0xeb
        self.spinBox_8.setValue(tmp2)
        self.spinBox_yz_5.setValue(tmp2)

        if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五格式
            self.spinBox_9.setValue(0x0506)
        else:
            self.spinBox_9.setValue(0x0106)
        
        self.spinBox_yz_6.setValue(0x0506)  # 延时
        self.on_btn_xor_clicked()  # 自动求累加和


    def on_btn_odu_time_update_3(self):   # 积分时间3修改
        i_time = self.doubleSpinBox_odu_time.value()  # 
        i_time_hex = int(i_time * 2)
        self.spinBox_odu_time_hex.setValue(i_time_hex)
        self.spinBox_5.setValue(0x0f07)
        self.spinBox_yz_2.setValue(0x0f07)  # 延时注数

        tmp1 = (i_time_hex << 8) & 0xff00
        tmp2 = tmp1 | i_time_hex
        self.spinBox_6.setValue(tmp2)
        self.spinBox_7.setValue(tmp2)
        self.spinBox_yz_3.setValue(tmp2)
        self.spinBox_yz_4.setValue(tmp2)


        tmp2 = tmp1 | 0xeb
        self.spinBox_8.setValue(tmp2)
        self.spinBox_yz_5.setValue(tmp2)

        if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五格式
            self.spinBox_9.setValue(0x0507)
        else:
            self.spinBox_9.setValue(0x0107)

        self.spinBox_yz_6.setValue(0x0507)  # 延时
        self.on_btn_xor_clicked()  # 自动求累加和

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
         
        if 0 == self.comboBox_djfreq.currentIndex():  # 20k
            djfreq_H = 0x02
            djfreq_L = 0x29EB
        else:   # 40k
            djfreq_H = 0x01
            djfreq_L = 0x14eb

        # 高低字节拼接
        apdata2 = ((djmode << 8) & 0xff00) | djpulse
        apdata3 = ((djpower << 8) & 0xff00) | djfreq_H
        apdata4 = djfreq_L

        # 更新数值 数据注入
        self.spinBox_5.setValue(0xcc37)
        self.spinBox_6.setValue(apdata2)
        self.spinBox_7.setValue(apdata3)
        self.spinBox_8.setValue(apdata4)

        # 更新数值 延时注数
        self.spinBox_yz_2.setValue(0xcc37)
        self.spinBox_yz_3.setValue(apdata2)
        self.spinBox_yz_4.setValue(apdata3)
        self.spinBox_yz_5.setValue(apdata4)
        self.spinBox_yz_6.setValue(0x1507)


        if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五格式
            self.spinBox_9.setValue(0x1507)
        else:
            self.spinBox_9.setValue(0x1107)

        self.on_btn_xor_clicked()  # 自动求累加和

        
    def on_btn_djrpm_clicked(self):  # 电机转速设置
        self.spinBox_5.setValue(0xcc38)
        self.spinBox_6.setValue(self.spinBox_dj_start_rpm.value())
        self.spinBox_7.setValue(self.spinBox_dj_work_rpm.value())
        self.spinBox_8.setValue(0xebeb)
        if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五格式
            self.spinBox_9.setValue(0x1508)
        else:
            self.spinBox_9.setValue(0x1108)

        self.spinBox_yz_2.setValue(0xcc38)
        self.spinBox_yz_3.setValue(self.spinBox_dj_start_rpm.value())
        self.spinBox_yz_4.setValue(self.spinBox_dj_work_rpm.value())
        self.spinBox_yz_5.setValue(0xebeb)
        self.spinBox_yz_6.setValue(0x1508)

        self.on_btn_xor_clicked()


    def on_btn_djrelay_clicked(self):  # 延时时间设置
        self.spinBox_5.setValue(0xcc39)
        self.spinBox_6.setValue(self.spinBox_dj_relay.value())
        self.spinBox_7.setValue(0xebeb)
        self.spinBox_8.setValue(0xebeb)
        if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五格式
            self.spinBox_9.setValue(0x1509)
        else:
            self.spinBox_9.setValue(0x1109)
        #延时
        self.spinBox_yz_2.setValue(0xcc39)
        self.spinBox_yz_3.setValue(self.spinBox_dj_relay.value())
        self.spinBox_yz_4.setValue(0xebeb)
        self.spinBox_yz_5.setValue(0xebeb)
        self.spinBox_yz_6.setValue(0x1509)

        self.on_btn_xor_clicked()

        

    def on_btn_djpos_clicked(self):  # 圈帧同步脉冲发送位置设置
        apdata = ((self.spinBox_dj_loop_width.value() << 8) & 0xff00) | 0xeb

        self.spinBox_5.setValue(0xcc3a)
        self.spinBox_6.setValue(self.spinBox_dj_loop_pos.value())
        self.spinBox_7.setValue(self.spinBox_dj_frame_pos.value())
        self.spinBox_8.setValue(apdata)
        if self.radioButton_gfdpc_yzfmt.isChecked():  # 选择高五格式
            self.spinBox_9.setValue(0x150a)
        else:
            self.spinBox_9.setValue(0x110a)
        # 延时
        self.spinBox_yz_2.setValue(0xcc3a)
        self.spinBox_yz_3.setValue(self.spinBox_dj_loop_pos.value())
        self.spinBox_yz_4.setValue(self.spinBox_dj_frame_pos.value())
        self.spinBox_yz_5.setValue(apdata)
        self.spinBox_yz_6.setValue(0x150a)

        self.on_btn_xor_clicked()



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

    # DN值转温度值 内部函数
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
        # 将阈值填充到单路加热器设置的阈值中
        if self.radioButton_wk_low.isChecked():  
            self.spinBox_wk_htlow.setValue(dn)  # 填充进入低温阈值
        else:
            self.spinBox_wk_hthigh.setValue(dn) # 填充进入高温阈值

    def on_btn_wk_dn2t_clicked(self):  # DN转温度
        resup = self.spinBox_wk_res_up.value()
        dnmax = self.spinBox_wk_dnmax.value()

        dn = self.spinBox_temperautre_dn.value()

        t = self.dn2t(dn, resup, dnmax)

        self.doubleSpinBox_temperautre_t.setValue(t)

    def on_btn_dpcmode_clicked(self):  # 修改工作模式
        mode_index = self.comboBox_dpcmode_1.currentIndex()
        sheet_index = self.comboBox_dpcmode_2.currentIndex()

        if mode_index == 0:  # 在轨存储
            apdata = 0x11eb            
        elif mode_index == 1:  # 待机模式
            apdata = 0x22eb
        elif mode_index == 2:  # 成像模式 开始判断流程表
            mode = 0x33
            if sheet_index == 0:  # 独立观测
                sheet = 0x1e
            elif sheet_index == 1:  # 交火观测
                sheet = 0x1f
            elif sheet_index == 2:  # 受控观测
                sheet = 0x1d
            else:
                sheet = 0xeb

            apdata = ((mode << 8) & 0xff00) | sheet

        else:
            pass               

        self.spinBox_5.setValue(0x1103)
        self.spinBox_6.setValue(apdata)
        self.spinBox_7.setValue(0xebeb)
        self.spinBox_8.setValue(0xebeb)
        self.spinBox_9.setValue(0xffff)

        #延时
        self.spinBox_yz_2.setValue(0x1103)
        self.spinBox_yz_3.setValue(apdata)
        self.spinBox_yz_4.setValue(0xebeb)
        self.spinBox_yz_5.setValue(0xebeb)
        self.spinBox_yz_6.setValue(0xffff)

        self.on_btn_xor_clicked()



    def on_btn_orbit_clicked(self):  # 修改轨道序号
        self.spinBox_5.setValue(0x1106)
        self.spinBox_6.setValue(0xebeb)
        self.spinBox_7.setValue(0xebeb)
        self.spinBox_8.setValue(self.spinBox_orbit.value())
        self.spinBox_9.setValue(0xffff)
        #延时
        self.spinBox_yz_2.setValue(0x1106)
        self.spinBox_yz_3.setValue(0xebeb)
        self.spinBox_yz_4.setValue(0xebeb)
        self.spinBox_yz_5.setValue(self.spinBox_orbit.value())
        self.spinBox_yz_6.setValue(0xffff)

        self.on_btn_xor_clicked()

    def on_btn_orbit_time_clicked(self): # 计算轨道周期
        orbit_time = self.doubleSpinBox_orbittime.value()
        orbit_time_dn = orbit_time*60*1000/0.1
        self.spinBox_orbittime_dn.setValue(int(orbit_time_dn))

    def on_btn_wk_htmode_click(self):  # 单路温控模式修改
        if 0 == self.comboBox_wk_htmode.currentIndex():  # 选择单路加热模式
            htmode = 0x55
        elif 1 == self.comboBox_wk_htmode.currentIndex():
            htmode = 0xf1
        elif 2 == self.comboBox_wk_htmode.currentIndex():           
            htmode = 0xa0
        else:
            pass
        
        htnum = self.spinBox_wk_htnum.value()

        apdata2 = ((htnum << 8) & 0xff00) | (htmode & 0x00ff) # 左移8位 
        self.spinBox_6.setValue(apdata2) 

        self.spinBox_5.setValue(0x3356)
        self.spinBox_7.setValue(0xebeb)
        self.spinBox_8.setValue(0xebeb)
        self.spinBox_9.setValue(0xffff)


    def on_btn_wk_resnum_click(self):  # 热敏电阻与加热器对应关系修改
        htnum = self.spinBox_wk_htnum.value()
        resnum = self.spinBox_wk_resnum.value()

        apdata2 = ((htnum << 8) & 0xff00) | (resnum & 0x00ff) # 左移8位 
        self.spinBox_6.setValue(apdata2)

        self.spinBox_5.setValue(0x3357)
        self.spinBox_7.setValue(0xebeb)
        self.spinBox_8.setValue(0xebeb)
        self.spinBox_9.setValue(0xffff)


    def on_btn_wk_htthrehold_click(self):  # 温控阈值调整
        # 获取高低温阈值
        htnum = self.spinBox_wk_htnum.value()
        high_thr = self.spinBox_wk_hthigh.value()
        low_thr = self.spinBox_wk_htlow.value()

        if high_thr > low_thr :
            QMessageBox.information(self, '阈值设置异常', 'DN值高温应小于低温')
        else:            
            ap2data = ((htnum << 8) & 0xff00) | ((high_thr >> 8) & 0x00ff)  # 高温阈值高8位 放在低8位
            ap3data = ((high_thr << 8) & 0xff00) | ((low_thr >> 8) & 0x00ff) # 高温阈值低8位 放在高8位   低温阈值高8位 放在低8位
            ap4data = ((low_thr << 8) & 0xff00) | 0x00eb  # 低温阈值低8位 放在高8位

            self.spinBox_5.setValue(0x3358)
            self.spinBox_6.setValue(ap2data)
            self.spinBox_7.setValue(ap3data)
            self.spinBox_8.setValue(ap4data)
            self.spinBox_9.setValue(0xffff)
    
    #  清空日志函数
    def on_btn_clear(self):
        self.textBrowser_log.clear()
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywidget = Test()
    mywidget.show()
    sys.exit(app.exec_())
