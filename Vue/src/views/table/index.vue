<template>
  <div class="app-container" accordion>
    <el-card>
      <!-- 手风琴 -->
      <el-collapse v-model="activeName">
        <el-collapse-item title="信息管理" name="1">
          <!-- 搜索 添加 -->
          <el-row :gutter="60">
            <el-col :md="6" :xs="24">
              <el-input
                placeholder="请输入内容"
                v-model="keywords"
                clearable
                @clear="getAllList"
                @keyup.enter.native="getAllList"
              >
                <el-button
                  slot="append"
                  icon="el-icon-search"
                  @click="getAllList"
                ></el-button>
              </el-input>
            </el-col>
            <el-col :md="2" :xs="6">
              <el-button type="success" @click="addDialogVisible = true"
                >添加</el-button
              >
            </el-col>
            <el-col :md="3" :xs="8">
              <a :href="'/cmdb/downloadInfo/'" download=""
                ><el-button type="primary" @click.stop
                  >导出Excel文件</el-button
                ></a
              >
            </el-col>
            <el-col :md="7" :xs="24">
              <el-alert
                show-icon
                title="注意：红色背景代表已闭店"
                type="warning"
                :closable="false"
              >
              </el-alert>
            </el-col>
          </el-row>
          <!-- 表格 -->
          <el-table
            :row-class-name="tableRowClassname"
            v-loading="loading"
            :data="
              allList.slice(
                (currentPage - 1) * pageSize,
                currentPage * pageSize
              )
            "
            height="700"
            @sort-change="changeSort"
            border
            stripe
            class="mt-10"
          >
            <!-- <el-table-column type="index" label="#"></el-table-column> -->
            <el-table-column type="expand">
              <template slot-scope="props">
                <i
                  data-clipboard-action="copy"
                  class="el-icon-copy-document cobyDomObj"
                  data-clipboard-target=".demo-expand"
                  @click="copyLink"
                ></i>
                <el-checkbox-group v-model="checkList">
                  <el-checkbox label="店铺号"></el-checkbox>
                  <el-checkbox label="ip地址"></el-checkbox>
                  <el-checkbox label="区域"></el-checkbox>
                  <el-checkbox label="tc51"></el-checkbox>
                  <el-checkbox label="vlan10"></el-checkbox>
                  <el-checkbox label="loopback IP"></el-checkbox>
                  <el-checkbox label="地址"></el-checkbox>
                  <el-checkbox label="型号"></el-checkbox>
                  <el-checkbox label="sn"></el-checkbox>
                  <el-checkbox label="Tunnel IP"></el-checkbox>
                  <el-checkbox label="监控日期"></el-checkbox>
                  <el-checkbox label="上网方式"></el-checkbox>
                  <el-checkbox label="ADSL IP"></el-checkbox>
                  <el-checkbox label="adslgateway"></el-checkbox>
                  <el-checkbox label="adslusername"></el-checkbox>
                  <el-checkbox label="adslpassword"></el-checkbox>
                </el-checkbox-group>
                <div class="demo-expand">
                  <div v-for="item in checkList" :key="item.id">
                    <span>{{ item }}:</span>
                    <span>{{ checkValuess(item, props.row) }}</span>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="店铺名"></el-table-column>
            <el-table-column
              prop="storenumber"
              label="店铺号" width="70"
            ></el-table-column>
            <el-table-column prop="vlan1" label="ip地址"></el-table-column>
            <el-table-column prop="region" label="区域" width="70"></el-table-column>
            <el-table-column
              prop="loopback"
              label="loopback IP"
            ></el-table-column>
            <el-table-column
              prop="modify_time"
              label="修改日期"
              sortable
            ></el-table-column>
            <el-table-column prop="opendate" label="开店日期"></el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="showEditLog(scope.row)"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  size="mini"
                  @click="deleteLog(scope.row.id)"
                  circle
                ></el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[30, 50, 100]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
          >
          </el-pagination>
        </el-collapse-item>
        <el-collapse-item title="批量管理" name="2">
          <div class="managerBatch">
            <div class="button-group">
              <a :href="'/cmdb/downloadExampleInfo/'" download="">
                <el-button round @click.stop>下载模板</el-button>
              </a>
            </div>
            <!-- 单选框 -->
            <el-radio-group v-model="radioUpload">
              <el-radio :label="2">批量添加</el-radio>
              <el-radio :label="1">批量替换</el-radio>
            </el-radio-group>
            <!-- 上传框 -->
            <el-upload
              class="image-uploader"
              :multiple="false"
              :auto-upload="true"
              list-type="text"
              :show-file-list="true"
              :before-upload="beforeUpload"
              :drag="true"
              action=""
              :limit="1"
              :on-exceed="handleExceed"
              :http-request="uploadFile"
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">
                将文件拖到此处，或<em>点击上传</em>
              </div>
              <div class="el-upload__tip" slot="tip">
                一次只能上传一个文件，仅限Excel格式
              </div>
            </el-upload>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 添加信息的对话框 -->
    <el-dialog
      title="添加"
      :visible.sync="addDialogVisible"
      width="60%"
      @close="diglogClose('add')"
    >
      <el-form
        :model="addForm"
        label-width="100px"
        :rules="addRules"
        ref="addRef"
      >
        <el-row>
          <el-col :md="8" :sm="24">
            <el-form-item label="店铺名" prop="name">
              <el-input
                v-model="addForm.name"
                placeholder="WTCCN-EC-368"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="店铺号" prop="storenumber">
              <el-input
                v-model="addForm.storenumber"
                placeholder="368"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="备注">
              <el-input v-model="addForm.mark"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="loopback" prop="loopback">
              <el-input
                v-model="addForm.loopback"
                placeholder="172.19.250.170/32"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="IP网段" prop="vlan1">
              <el-input
                v-model="addForm.vlan1"
                placeholder="10.67.25.193/26"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="Tunnel IP" prop="tunnelip">
              <el-input
                v-model="addForm.tunnelip"
                placeholder="10.67.203.40/30;10.67.203.44/30"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="S/N号">
              <el-input
                v-model="addForm.sn"
                placeholder="FHK13527ATU"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="tc51">
              <el-input
                v-model="addForm.tc51"
                placeholder="10.84.216.193/26"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="Vlan 10">
              <el-input
                v-model="addForm.vlan10"
                placeholder="10.82.250.96/27"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="店铺区域" prop="region">
              <el-select v-model="addForm.region" placeholder="请选择店铺区域">
                <el-option label="EC" value="EC"></el-option>
                <el-option label="SC" value="SC"></el-option>
                <el-option label="WC" value="WC"></el-option>
                <el-option label="NC" value="NC"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="店铺地址" prop="address">
              <el-input
                v-model="addForm.address"
                clearable
                placeholder="上海市东江区乐都路路378号"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="监控日期" prop="monidate">
              <el-date-picker
                v-model="addForm.monidate"
                type="date"
                placeholder="选择日期"
                format="yyyy年MM月dd日"
                value-format="yyyy年MM月dd日"
              >
                >
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="开店日期" prop="opendate">
              <el-date-picker
                v-model="addForm.opendate"
                type="date"
                placeholder="选择日期"
                format="yyyy年MM月dd日"
                value-format="yyyy年MM月dd日"
              >
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="门店类型" prop="model">
              <el-select v-model="addForm.model" placeholder="请选择门店类型">
                <el-option label="891F" value="891F"></el-option>
                <el-option label="891" value="891"></el-option>
                <el-option label="887" value="887"></el-option>
                <el-option label="1811" value="1811"></el-option>
                <el-option label="SDWAN-887" value="SDWAN-887"></el-option>
                <el-option label="SDWAN-891" value="SDWAN-891"></el-option>
                <el-option label="SDWAN-891F" value="SDWAN-891F"></el-option>
                <el-option label="SDWAN-1811" value="SDWAN-1811"></el-option>
                <el-option label="SDWAN" value="SDWAN"></el-option>
                <el-option label="OFF" value="OFF"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="上网方式" prop="internet">
              <el-select
                v-model="addForm.internet"
                placeholder="请选择上网方式"
              >
                <el-option label="拨号" value="拨号"></el-option>
                <el-option label="DHCP" value="DHCP"></el-option>
                <el-option label="固定IP" value="固定IP"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-show="addForm.internet === '拨号'">
          <el-col :md="12" :sm="24">
            <el-form-item label="宽带账号">
              <el-input v-model="addForm.adslusername"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="宽带密码">
              <el-input v-model="addForm.adslpassword"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-show="addForm.internet === '固定IP'">
          <el-col :md="12" :sm="24">
            <el-form-item label="固定IP">
              <el-input v-model="addForm.adslip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="网关">
              <el-input v-model="addForm.adslgateway"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-show="addForm.internet === 'DHCP'">
          <el-col :md="12" :sm="24">
            <el-form-item label="网关">
              <el-input v-model="addForm.adslgateway"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addLog">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 修改信息的对话框 -->
    <el-dialog
      title="修改"
      :visible.sync="editDialogVisible"
      width="60%"
      @close="diglogClose('edit')"
    >
      <el-form
        :model="editForm"
        label-width="100px"
        :rules="editRules"
        ref="editRef"
      >
        <el-row>
          <el-col :md="8" :sm="24">
            <el-form-item label="店铺名" prop="name">
              <el-input
                v-model="editForm.name"
                placeholder="WTCCN-EC-368"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="店铺号" prop="storenumber">
              <el-input
                v-model="editForm.storenumber"
                placeholder="368"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="备注">
              <el-input v-model="editForm.mark"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="loopback" prop="loopback">
              <el-input
                v-model="editForm.loopback"
                placeholder="172.19.250.170/32"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="IP网段" prop="vlan1">
              <el-input
                v-model="editForm.vlan1"
                placeholder="10.67.25.193/26"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="Tunnel IP" prop="tunnelip">
              <el-input
                v-model="editForm.tunnelip"
                placeholder="10.67.203.40/30;10.67.203.44/30"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="S/N号">
              <el-input
                v-model="editForm.sn"
                placeholder="FHK13527ATU"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="tc51">
              <el-input v-model="editForm.tc51" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="Vlan 10">
              <el-input v-model="editForm.vlan10"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="店铺区域" prop="region">
              <el-select v-model="editForm.region" placeholder="请选择店铺区域">
                <el-option label="EC" value="EC"></el-option>
                <el-option label="SC" value="SC"></el-option>
                <el-option label="WC" value="WC"></el-option>
                <el-option label="NC" value="NC"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="店铺地址" prop="address">
              <el-input
                v-model="editForm.address"
                clearable
                placeholder="上海市东江区乐都路路378号"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="监控日期" prop="monidate">
              <el-date-picker
                v-model="editForm.monidate"
                type="date"
                placeholder="选择日期"
                format="yyyy年MM月dd日"
                value-format="yyyy年MM月dd日"
              >
                >
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="开店日期" prop="opendate">
              <el-date-picker
                v-model="editForm.opendate"
                type="date"
                placeholder="选择日期"
                format="yyyy年MM月dd日"
                value-format="yyyy年MM月dd日"
              >
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="门店类型" prop="model">
              <el-select v-model="editForm.model" placeholder="请选择门店类型">
                <el-option label="891F" value="891F"></el-option>
                <el-option label="891" value="891"></el-option>
                <el-option label="887" value="887"></el-option>
                <el-option label="1811" value="1811"></el-option>
                <el-option label="SDWAN-887" value="SDWAN-887"></el-option>
                <el-option label="SDWAN-891" value="SDWAN-891"></el-option>
                <el-option label="SDWAN-891F" value="SDWAN-891F"></el-option>
                <el-option label="SDWAN-1811" value="SDWAN-1811"></el-option>
                <el-option label="SDWAN" value="SDWAN"></el-option>
                <el-option label="OFF" value="OFF"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="上网方式" prop="internet">
              <el-select
                v-model="editForm.internet"
                placeholder="请选择上网方式"
              >
                <el-option label="拨号" value="拨号"></el-option>
                <el-option label="DHCP" value="DHCP"></el-option>
                <el-option label="固定IP" value="固定IP"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-show="editForm.internet === '拨号'">
          <el-col :md="12" :sm="24">
            <el-form-item label="宽带账号">
              <el-input v-model="editForm.adslusername"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="宽带密码">
              <el-input v-model="editForm.adslpassword"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-show="editForm.internet === '固定IP'">
          <el-col :md="12" :sm="24">
            <el-form-item label="固定IP">
              <el-input v-model="editForm.adslip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="网关">
              <el-input v-model="editForm.adslgateway"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-show="editForm.internet === 'DHCP'">
          <el-col :md="12" :sm="24">
            <el-form-item label="网关">
              <el-input v-model="editForm.adslgateway"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editLog">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import _ from 'lodash'
export default {
  data() {
    return {
      keywords: "",
      allList: [],
      addDialogVisible: false,
      //手风琴
      activeName: "1",
      total: 1,
      //当前页数
      currentPage: 1,
      pageSize: 30,
      addForm: {
        name: "",
        region: "",
        address: "",
        vlan1: "",
        model: "",
        opendate: "",
        monidate: "",
        internet: "",
        adslusername: "",
        adslpassword: "",
        storenumber: "",
        loopback: "",
        tunnelip: "",
        sn: "",
        tc51: "",
        vlan10: "",
        mark: "",
        adslip: "",
        adslgateway: ""
      },
      //添加信息表单规则
      addRules: {
        name: { required: true, message: "请输入店铺名", trigger: "blur" },
        region: { required: true, message: "请输入区域", trigger: "blur" },
        address: { required: true, message: "请输入地址", trigger: "blur" },
        vlan1: { required: true, message: "请输入IP地址", trigger: "blur" },
        model: { required: true, message: "请输入型号", trigger: "blur" },
        opendate: {
          required: true,
          message: "请输入开店日期",
          trigger: "blur"
        },
        monidate: {
          required: true,
          message: "请输入监控日期",
          trigger: "blur"
        },
        internet: {
          required: true,
          message: "请输入上网方式",
          trigger: "blur"
        },
        loopback: {
          required: true,
          message: "请输入loopback地址",
          trigger: "blur"
        },
        tunnelip: {
          required: true,
          message: "请输入tunnel IP",
          trigger: "blur"
        },
        // sn: { required: true, message: "请输入S/N号", trigger: "blur" },
        storenumber: {
          required: true,
          message: "请输入店铺号",
          trigger: "blur"
        }
      },
      editRules: {
        name: { required: true, message: "请输入店铺名", trigger: "blur" },
        region: { required: true, message: "请输入区域", trigger: "blur" },
        address: { required: true, message: "请输入地址", trigger: "blur" },
        vlan1: { required: true, message: "请输入IP地址", trigger: "blur" },
        model: { required: true, message: "请输入型号", trigger: "blur" },
        internet: {
          required: true,
          message: "请输入上网方式",
          trigger: "blur"
        },
        loopback: {
          required: true,
          message: "请输入loopback地址",
          trigger: "blur"
        },
        tunnelip: {
          required: true,
          message: "请输入tunnel IP",
          trigger: "blur"
        },
        // sn: { required: true, message: "请输入S/N号", trigger: "blur" },
        storenumber: {
          required: true,
          message: "请输入店铺号",
          trigger: "blur"
        }
      },
      editForm: {},
      editDialogVisible: false,
      loading: false,
      // 需要显示的label和对应的值
      dict: {
        店铺号: "storenumber",
        ip地址: "vlan1",
        "loopback IP": "loopback",
        地址: "address",
        区域: "region",
        tc51: "tc51",
        vlan10: "vlan10",
        区域: "region",
        型号: "model",
        sn: "sn",
        "Tunnel IP": "tunnelip",
        监控日期: "monidate",
        上网方式: "internet",
        "ADSL IP": "adslip",
        adslgateway: "adslgateway",
        adslusername: "adslusername",
        adslpassword: "adslpassword"
      },
      //扩展列显示列表
      checkList: [],
      // 批量管理单选框
      radioUpload: 2
    };
  },
  computed: {},
  mounted() {
    // 初始化多选项显示列表
    this.checkList = Object.keys(this.dict);
    this.getAllList();
  },
  methods: {
    changeSort(val){
      let sortData=_.cloneDeep(this.allList)
      if(val.order==="descending"){
        if(val.prop==="modify_time"){
          // console.log(val.prop)
          sortData.sort(this.sortKeys(val.prop,true))
          // console.log(sortData)
        }
      }else{
        if(val.prop==="modify_time"){
          sortData.sort(this.sortKeys(val.prop,false))
        }
      }
      this.allList=sortData
      // this.currentPage=1
    },
    // 升序降序
    sortKeys(key,order){
      if(order){
        return (val1,val2)=>{
          return val2[key] > val1[key] ? 1 : -1
        }
      }else{
        return (val1,val2)=>{
          return val2[key] < val1[key] ? 1 : -1
        }
      }
    },
    checkValuess(item, info) {
      let k = this.dict[item];
      // console.log(k,info)
      return info[k];
    },
    //高亮显示闭店
    tableRowClassname({ row, rowIndex }) {
      // console.log(row);
      if (row.model.indexOf("OFF") > -1) {
        return "warning-row";
      }
      return "";
    },
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    copyLink() {
      let _this = this;
      let clipboardObj = new this.clipboard(".cobyDomObj");
      clipboardObj.on("success", function() {
        // console.log(success)
        _this.$message.success("复制成功");
      });
      clipboardObj.on("error", function() {
        _this.$message.error("复制失败");
      });
    },
    //获取info表
    async getAllList() {
      this.loading = true;
      await this.$request({
        url: "/cmdb/searchBySome/",
        method: "get",
        params:{
          query:this.keywords
        }
      })
        .then(res => {
          console.log(res.data)
          res.data.map(item => {
            item.modify_time = item.modify_time.replace("T", " ");
          });
          this.allList=res.data
          // console.log(this.allList)
          this.total = this.allList.length;
          this.currentPage = 1
          this.loading = false;
        })
        .catch(err => {
          this.loading = false;
        });
    },
    //添加记录
    addLog() {
      this.$refs.addRef.validate(async valid => {
        if (!valid) return;
        await this.$request({
          url: "/cmdb/insertInfo/",
          method: "post",
          data: this.addForm
        }).then(res => {
          this.$message.success("添加记录成功");
          res.data.forEach(item => {
            item.modify_time = item.modify_time.replace("T", " ");
          });
          this.allList = res.data;
          this.total = this.allList.length;
        });
        this.addDialogVisible = false;
      });
    },
    //显示修改对话框
    showEditLog(info) {
      this.editForm = info;
      this.editDialogVisible = true;
    },
    //发送修改数据请求
    editLog() {
      this.$refs.editRef.validate(async valid => {
        if (!valid) return;
        // console.log(this.editForm);
        await this.$request({
          url: "/cmdb/updateInfo/",
          method: "post",
          data: this.editForm
        }).then(res => {
          this.$message.success("修改记录成功");
          res.data.forEach(item => {
            item.modify_time = item.modify_time.replace("T", " ");
          });
          this.allList = res.data;
          this.total = this.allList.length;
        });
        this.editDialogVisible = false;
      });
    },
    async deleteLog(id) {
      const confirmResult = await this.$confirm(
        "此操作将永久删除该信息, 是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        }
      ).catch(err => err);
      // 点击确定 返回值为：confirm
      // 点击取消 返回值为： cancel
      if (confirmResult !== "confirm") {
        return this.$message.info("已取消删除");
      }
      await this.$request({
        url: "/cmdb/deleteById/",
        method: "delete",
        data: {
          id: id
        }
      }).then(res => {
        res.data.forEach(item => {
          item.modify_time = item.modify_time.replace("T", " ");
        });
        this.allList = res.data;
        this.total = this.allList.length;
        this.$nextTick(() => {
          this.$message.success("删除记录成功");
        });
      });
    },
    //监听对话框监听事件
    diglogClose(event) {
      if (event === "add") {
        this.$refs.addRef.resetFields();
        this.addForm = {
          name: "",
          region: "",
          address: "",
          vlan1: "",
          model: "",
          opendate: "",
          monidate: "",
          internet: "",
          adslusername: "",
          adslpassword: "",
          storenumber: "",
          loopback: "",
          tunnelip: "",
          sn: "",
          tc51: "",
          vlan10: "",
          mark: "",
          adslip: "",
          adslgateway: ""
        };
      } else if (event === "edit") {
        this.$refs.editRef.resetFields();
        this.editForm = {};
      }
    },
    // 上传文件之前的钩子
    beforeUpload(file) {
      //判断文件格式
      let hz = file.name.split(".")[1];
      if (hz != "xlsx" && hz != "xls" && hz != "csv") {
        this.$message.info("请上传正确的Excel文件");
        return false;
      }
    },
    // 上传文件个数超过定义的数量
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，请删除后继续上传`);
    },
    // 上传文件
    uploadFile(item) {
      if (!this.radioUpload) {
        return this.$message.error("请选择选项");
      }
      let fileObj = item.file;
      const form = new FormData(); // FormData 对象
      form.append("info_file", fileObj); // 文件对象  'upload'是后台接收的参数名
      form.append("type", this.radioUpload);
      this.$request({
        url: "/cmdb/uploadInfo/",
        data: form,
        method: "post",
        headers: {
          "Content-type": "multipart/form-data"
        }
      })
        .then(res => {
          this.getAllList();
          this.$message.success("上传成功！！请检查数据是否修改");
          // console.log(res);
        })
        .catch(err => {
          this.$message.error("失败，请上传正确的文件！！");
        });
    }
  }
};
</script>
<style lang="scss" scoped>
.el-table .warning-row {
  background: #fd7201;
}
// .demo-table-expand {
//   font-size: 0;
//   label {
//     width: 90px;
//     color: #99a9bf;
//   }
//   .el-form-item {
//     margin-right: 0;
//     margin-bottom: 0;
//     width: 50%;
//   }
// }
.demo-expand {
  div {
    margin: 0;
    span:nth-child(1) {
      color: #99a9bf;
      display: inline-block;
      width: 130px;
    }
  }
}
.cobyDomObj {
  margin-left: -27px;
  color: #123abc;
  font-size: 16px;
}
.managerBatch {
  padding: 10px;
  text-align: center;
  border: 1px solid #eee;
  .button-group {
    padding-bottom: 15px;
    display: flex;
    justify-content: space-around;
  }
  .el-radio-group {
    padding-bottom: 15px;
  }
  .image-uploader {
    overflow: auto;
  }
  /deep/ .el-upload-dragger {
    width: 100%;
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>
