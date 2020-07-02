<template>
  <div class="app-container">
    <el-card>
      <el-tabs v-model="activeName" @tab-click="tabActiveClick">
        <el-tab-pane label="智能查询" name="check">
          <!-- 搜索 添加 -->
          <el-row :gutter="10">
            <el-col :md="6" :xs="15">
              <el-input
                placeholder="输入你要查询的店铺号"
                v-model.trim="formInline.stores"
                clearable
              >
              </el-input>
            </el-col>
            <el-col :md="3" :xs="3">
              <el-button type="primary" @click="onCheck" :loading="checkLoading"
                >查询</el-button
              >
            </el-col>
          </el-row>
          <el-row>
            <el-col :xs="24" :lg="14" class="info-group">
              <p>店铺基本信息：</p>
              <table class="info" v-if="StoreInfo" width="100%">
                <tr>
                  <td>店铺号码：{{ StoreInfo.stores }}</td>
                  <td>区域：{{ StoreInfo.area }}</td>
                </tr>
                <tr>
                  <td colspan="2">地址：{{ StoreInfo.address }}</td>
                </tr>
                <tr>
                  <td colspan="2">联系方式：{{ StoreInfo.stores_phone }}</td>
                </tr>
                <tr>
                  <td>区域IT：{{ StoreInfo.manager }}</td>
                  <td>区域联系方式：{{ StoreInfo.manager_phone }}</td>
                </tr>
                <tr>
                  <td>路由器类型：{{ StoreInfo.router }}</td>
                  <td>IP：{{ StoreInfo.router_ip }}</td>
                </tr>
                <tr>
                  <td>AP类型：{{ StoreInfo.ap_type }}</td>
                  <td>AP数量：{{ StoreInfo.ap_count }}</td>
                </tr>
                <tr v-for="(val, key, index) in StoreInfo.ap" :key="index">
                  <td>{{ key }} 类型：{{ val[0] }}</td>
                  <td>{{ key }} IP：{{ val[1] }}</td>
                </tr>
              </table>
            </el-col>
          </el-row>
          <el-row>
            <el-col :xs="24" :lg="14" class="check-group">
              <p>实时网络检查：</p>
              <div
                class="check-result"
                v-if="result"
                v-loading="checkLoading"
                 element-loading-text="拼命加载中"
              >
                <el-table :data="result" border>
                  <el-table-column type="expand">
                    <template slot-scope="props">
                      <div
                        v-html="$options.filters.ExpandContent(props.row.value)"
                      ></div>
                    </template>
                  </el-table-column>
                  <el-table-column label="label">
                    <template slot-scope="props">
                      <div
                        v-html="
                          $options.filters.checkLabelContent(props.row.label)
                        "
                      ></div>
                    </template>
                  </el-table-column>
                  <el-table-column label="status">
                    <template slot-scope="props">
                      {{ props.row.value | checkStatusContent }}
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>



        <el-tab-pane label="联系方式" name="contact">
          <!-- 搜索 添加 -->
          <el-row>
            <el-col :md="6" :xs="15" class="input-mr-10">
              <el-input
                placeholder="请输入内容"
                v-model="contact.keywords"
                clearable
                @clear="getContactList"
                @keyup.enter.native="getContactList"
              >
              </el-input>
            </el-col>
            <el-col :md="2" :xs="6" class="input-mr-10">
            <el-button
                  type="primary"
                  icon="el-icon-search"
                  @click="getContactList"
                >搜索</el-button>
            </el-col>
            <el-col :md="2" :xs="6">
              <el-button type="primary" @click="contact.addVisible = true"
                >添加</el-button>
            </el-col>
            <el-col :md="3" :xs="3" >
              <el-button type="primary" @click="contact.addVisible = true"
                >下载模板<i class="el-icon-download"></i></el-button
              >
            </el-col>
            <el-col :md="3" :xs="3" >
              <el-button type="success" @click="contact.addVisible = true"
                >批量上传<i class="el-icon-upload el-icon--right"></i></el-button
              >
            </el-col>
          </el-row>
          <el-table
            :data="
              contactTable.slice(
                (contact.CurrPage - 1) * contact.PageSize,
                contact.CurrPage * contact.PageSize
              )
            "
            v-loading="contact.loading"
            stripe
            border
            style="width: 100%"
          >
            <el-table-column type="index"></el-table-column>
            <el-table-column prop="storeNO" label="店铺号" width="90">
            </el-table-column>
            <el-table-column label="区域" width="90">
              <template slot-scope="scope">
                <el-tag type="primary">{{ scope.row.region }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="联系方式">
              <template slot-scope="scope">
                <el-input
                  v-if="scope.row.isSet"
                  v-model="scope.row.telephone"
                  size="mini"
                />
                <span v-else>{{ scope.row.telephone }}</span>
              </template>
            </el-table-column>
            <el-table-column label="区域经理" width="90">
              <template slot-scope="scope">
                <el-input
                  v-if="scope.row.isSet"
                  v-model="scope.row.regional_manager"
                  size="mini"
                />
                <span v-else>{{ scope.row.regional_manager }}</span>
              </template>
            </el-table-column>
            <el-table-column label="区经电话" width="90">
              <template slot-scope="scope">
                <el-input
                  v-if="scope.row.isSet"
                  v-model="scope.row.regional_manager_phone"
                  size="mini"
                />
                <span v-else>{{ scope.row.regional_manager_phone }}</span>
              </template>
            </el-table-column>
            <el-table-column label="区域IT">
              <template slot-scope="scope">
                <el-input
                  v-if="scope.row.isSet"
                  v-model="scope.row.regional_it"
                  size="mini"
                />
                <span v-else>{{ scope.row.regional_it }}</span>
              </template>
            </el-table-column>
            <el-table-column label="IT电话">
              <template slot-scope="scope">
                <el-input
                  v-if="scope.row.isSet"
                  v-model="scope.row.regional_it_phone"
                  size="mini"
                />
                <span v-else>{{ scope.row.regional_it_phone }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button
                  type="primary"
                  plain
                  size="mini"
                  @click.native.prevent="
                    ContactUpdate(scope.row, scope.$index, true)
                  "
                  >{{ scope.row.isSet ? "保存" : "编辑" }}</el-button
                >
                <el-button
                  v-if="scope.row.isSet"
                  type="success"
                  plain
                  size="mini"
                  @click.native.prevent="
                    ContactUpdate(scope.row, scope.$index, false)
                  "
                  >取消</el-button
                >
                <el-button
                  v-if="!scope.row.isSet"
                  type="danger"
                  plain
                  size="mini"
                  @click.native.prevent="ContactDelete(scope.row.storeNO)"
                  >删除</el-button
                >
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            background
            @size-change="contactSizeChange"
            @current-change="contactCurrentChange"
            :current-page="contact.CurrPage"
            :page-sizes="[10, 30]"
            :page-size="contact.PageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="contact.Total"
          >
          </el-pagination>
        </el-tab-pane>



        <el-tab-pane label="设备信息" name="device">
          <!-- 搜索 添加 -->
          <el-row>
            <el-col :md="6" :xs="15" class="input-mr-10">
              <el-input
                placeholder="请输入内容"
                v-model="devices.keywords"
                clearable
                @clear="getDevicesList"
                @keyup.enter.native="getDevicesList"
              >
              </el-input>
            </el-col>
            <el-col :md="2" :xs="6" class="input-mr-10">
            <el-button
                  type="primary"
                  icon="el-icon-search"
                  @click="getDevicesList"
                >搜索</el-button>
            </el-col>
            <el-col :md="2" :xs="6">
              <el-button type="primary" @click="devices.addVisible = true"
                >添加</el-button
              >
            </el-col>
            <el-col :md="3" :xs="3" >
              <el-button type="primary" @click="contact.addVisible = true"
                >下载模板<i class="el-icon-download"></i></el-button
              >
            </el-col>
            <el-col :md="3" :xs="3" >
              <el-button type="success" @click="contact.addVisible = true"
                >批量上传<i class="el-icon-upload el-icon--right"></i></el-button
              >
            </el-col>
          </el-row>
          <el-table
            :data="
              devicesTable.slice(
                (devices.CurrPage - 1) * devices.PageSize,
                devices.CurrPage * devices.PageSize
              )
            "
            v-loading="devices.loading"
            stripe
            border
            style="width: 100%"
          >
            <el-table-column type="expand">
              <template slot-scope="scope">
                <p v-if="scope.row.router_version">Flash version: {{ scope.row.router_version }}</p>
                <p v-for="(val, key, index) in scope.row" :key="index">
                  {{
                    key.indexOf("ap") > -1 && val
                      ? `${key.toUpperCase()} : ${val}`
                      : ""
                  }}
                </p>
              </template>
            </el-table-column>
            <el-table-column prop="storeNO" label="店铺号" width="90"></el-table-column>
            <el-table-column prop="region" label="区域" width="90"></el-table-column>
            <el-table-column prop="router" label="门店类型"> </el-table-column>
            <el-table-column prop="router_ip" label="IP地址"> </el-table-column>
            <el-table-column prop="router_serial" label="S/N"> </el-table-column>
            <el-table-column label="是否Aruba" width="90">
              <template slot-scope="scope">
                <el-tag type="primary" v-if="scope.row.is_aruba === '是'"
                  >是</el-tag
                >
                <el-tag type="success" v-else>否</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="110">
              <template slot-scope="scope">
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="showEditDevices(scope.row)"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  size="mini"
                  @click="deleteDevices(scope.row.storeNO)"
                  circle
                ></el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            background
            @size-change="deviceSizeChange"
            @current-change="deviceCurrentChange"
            :current-page="devices.CurrPage"
            :page-sizes="[10, 30]"
            :page-size="devices.PageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="devices.Total"
          >
          </el-pagination>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <!-- 添加店铺联系方式 -->
    <el-dialog
      title="添加"
      :visible.sync="contact.addVisible"
      width="60%"
      @close="diglogClose('addContact')"
    >
      <el-form
        :model="contact.addForm"
        label-width="100px"
        :rules="contact.addRules"
        ref="addContactRef"
      >
        <el-row>
          <el-col :md="8" :sm="24">
            <el-form-item label="店铺号" prop="storeNO">
              <el-input
                v-model="contact.addForm.storeNO"
                placeholder="368"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="店铺区域" prop="region">
              <el-select
                v-model="contact.addForm.region"
                placeholder="请选择店铺区域"
              >
                <el-option label="EC" value="EC"></el-option>
                <el-option label="SC" value="SC"></el-option>
                <el-option label="WC" value="WC"></el-option>
                <el-option label="NC" value="NC"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="电话号码" prop="telephone">
              <el-input
                v-model="contact.addForm.telephone"
                placeholder="020-87395244"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="区域经理">
              <el-input v-model="contact.addForm.regional_manager"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="区经电话">
              <el-input
                v-model="contact.addForm.regional_manager_phone"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="区域IT" prop="regional_it">
              <el-input v-model="contact.addForm.regional_it"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="IT电话" prop="regional_it_phone">
              <el-input v-model="contact.addForm.regional_it_phone"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="contact.addVisible = false">取 消</el-button>
        <el-button type="primary" @click="addContact">确 定</el-button>
      </div>
    </el-dialog>
    <!-- 添加店铺设备信息 -->
    <el-dialog
      title="添加"
      :visible.sync="devices.addVisible"
      width="60%"
      @close="diglogClose('addDevice')"
    >
      <el-form
        :model="devices.addForm"
        label-width="100px"
        :rules="devices.addRules"
        ref="addDeviceRef"
      >
        <el-row>
          <el-col :md="8" :sm="24">
            <el-form-item label="店铺号" prop="storeNO">
              <el-input
                v-model="devices.addForm.storeNO"
                placeholder="368"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP数量">
              <el-select
                v-model="devices.addForm.apCount"
                placeholder="请选择AP数量"
              >
                <el-option label="1" value="1"></el-option>
                <el-option label="2" value="2"></el-option>
                <el-option label="3" value="3"></el-option>
                <el-option label="4" value="4"></el-option>
                <el-option label="5" value="5"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="是否Aruba">
              <el-select
                v-model="devices.addForm.is_aruba"
                placeholder="请选择是否Aruba"
              >
                <el-option label="是" value="是"></el-option>
                <el-option label="否" value=""></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="店铺区域" prop="region">
              <el-select v-model="devices.addForm.region" placeholder="请选择店铺区域">
                <el-option label="EC" value="EC"></el-option>
                <el-option label="SC" value="SC"></el-option>
                <el-option label="WC" value="WC"></el-option>
                <el-option label="NC" value="NC"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="门店类型" prop="router">
              <el-select v-model="devices.addForm.router">
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
            <el-form-item label="IP地址" prop="router_ip">
              <el-input v-model="devices.addForm.router_ip"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP01">
              <el-input v-model="devices.addForm.ap_1"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP01 IP">
              <el-input v-model="devices.addForm.ap_1_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP01版本">
              <el-input v-model="devices.addForm.ap_1_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP01型号">
              <el-input v-model="devices.addForm.ap_1_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP01序列号">
              <el-input v-model="devices.addForm.ap_1_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.addForm.apCount - 0 > 1">
          <el-col :md="8" :sm="24">
            <el-form-item label="AP02">
              <el-input v-model="devices.addForm.ap_2"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP02 IP">
              <el-input v-model="devices.addForm.ap_2_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP02版本">
              <el-input v-model="devices.addForm.ap_2_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.addForm.apCount - 0 > 1">
          <el-col :md="12" :sm="24">
            <el-form-item label="AP02型号">
              <el-input v-model="devices.addForm.ap_2_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP02序列号">
              <el-input v-model="devices.addForm.ap_2_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.addForm.apCount - 0 > 2">
          <el-col :md="8" :sm="24">
            <el-form-item label="AP03">
              <el-input v-model="devices.addForm.ap_3"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP03 IP">
              <el-input v-model="devices.addForm.ap_3_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP03版本">
              <el-input v-model="devices.addForm.ap_3_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.addForm.apCount - 0 > 2">
          <el-col :md="12" :sm="24">
            <el-form-item label="AP03型号">
              <el-input v-model="devices.addForm.ap_3_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP03序列号">
              <el-input v-model="devices.addForm.ap_3_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.addForm.apCount - 0 > 3">
          <el-col :md="8" :sm="24">
            <el-form-item label="AP04">
              <el-input v-model="devices.addForm.ap_4"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP04 IP">
              <el-input v-model="devices.addForm.ap_4_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP04版本">
              <el-input v-model="devices.addForm.ap_4_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.addForm.apCount - 0 > 3">
          <el-col :md="12" :sm="24">
            <el-form-item label="AP04型号">
              <el-input v-model="devices.addForm.ap_4_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP04序列号">
              <el-input v-model="devices.addForm.ap_4_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.addForm.apCount - 0 > 4">
          <el-col :md="8" :sm="24">
            <el-form-item label="AP05">
              <el-input v-model="devices.addForm.ap_5"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP05 IP">
              <el-input v-model="devices.addForm.ap_5_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP05版本">
              <el-input v-model="devices.addForm.ap_5_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.addForm.apCount - 0 > 4">
          <el-col :md="12" :sm="24">
            <el-form-item label="AP05型号">
              <el-input v-model="devices.addForm.ap_5_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP05序列号">
              <el-input v-model="devices.addForm.ap_5_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="devices.addVisible = false">取 消</el-button>
        <el-button type="primary" @click="addDevices">确 定</el-button>
      </div>
    </el-dialog>
    <!-- 编辑设备信息的对话框 -->
    <el-dialog
      title="添加"
      :visible.sync="devices.editVisible"
      width="60%"
      @close="diglogClose('editDevice')"
    >
      <el-form
        :model="devices.editForm"
        label-width="100px"
        :rules="devices.editRules"
        ref="editDeviceRef"
      >
        <el-row>
          <el-col :md="8" :sm="24">
            <el-form-item label="店铺号">
              <el-input v-model="devices.editForm.storeNO" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP数量">
              <el-select
                v-model="devices.editForm.apCount"
                placeholder="请选择AP数量"
              >
                <el-option label="1" value="1"></el-option>
                <el-option label="2" value="2"></el-option>
                <el-option label="3" value="3"></el-option>
                <el-option label="4" value="4"></el-option>
                <el-option label="5" value="5"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="是否Aruba">
              <el-select
                v-model="devices.editForm.is_aruba"
                placeholder="请选择是否Aruba"
              >
                <el-option label="是" value="是"></el-option>
                <el-option label="否" value=""></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="门店类型" prop="router">
              <el-select v-model="devices.editForm.router">
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
            <el-form-item label="IP地址" prop="router_ip">
              <el-input v-model="devices.editForm.router_ip"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP01">
              <el-input v-model="devices.editForm.ap_1"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP01 IP">
              <el-input v-model="devices.editForm.ap_1_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP01版本">
              <el-input v-model="devices.editForm.ap_1_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP01型号">
              <el-input v-model="devices.editForm.ap_1_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP01序列号">
              <el-input v-model="devices.editForm.ap_1_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>


        <el-row v-if="devices.editForm.apCount - 0 > 1">
          <el-col :md="8" :sm="24">
            <el-form-item label="AP02">
              <el-input v-model="devices.editForm.ap_2"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP02 IP">
              <el-input v-model="devices.editForm.ap_2_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP02版本">
              <el-input v-model="devices.editForm.ap_2_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.editForm.apCount - 0 > 1">
          <el-col :md="12" :sm="24">
            <el-form-item label="AP02型号">
              <el-input v-model="devices.editForm.ap_2_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP02序列号">
              <el-input v-model="devices.editForm.ap_2_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row v-if="devices.editForm.apCount - 0 > 2">
          <el-col :md="8" :sm="24">
            <el-form-item label="AP03">
              <el-input v-model="devices.editForm.ap_3"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP03 IP">
              <el-input v-model="devices.editForm.ap_3_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP03版本">
              <el-input v-model="devices.editForm.ap_3_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.editForm.apCount - 0 > 2">
          <el-col :md="12" :sm="24">
            <el-form-item label="AP03型号">
              <el-input v-model="devices.editForm.ap_3_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP03序列号">
              <el-input v-model="devices.editForm.ap_3_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row v-if="devices.editForm.apCount - 0 > 3">
          <el-col :md="8" :sm="24">
            <el-form-item label="AP04">
              <el-input v-model="devices.editForm.ap_4"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP04 IP">
              <el-input v-model="devices.editForm.ap_4_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP04版本">
              <el-input v-model="devices.editForm.ap_4_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.editForm.apCount - 0 > 3">
          <el-col :md="12" :sm="24">
            <el-form-item label="AP04型号">
              <el-input v-model="devices.editForm.ap_4_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP04序列号">
              <el-input v-model="devices.editForm.ap_4_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row v-if="devices.editForm.apCount - 0 > 4">
          <el-col :md="8" :sm="24">
            <el-form-item label="AP05">
              <el-input v-model="devices.editForm.ap_5"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP05 IP">
              <el-input v-model="devices.editForm.ap_5_ip"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="8" :sm="24">
            <el-form-item label="AP05版本">
              <el-input v-model="devices.editForm.ap_5_version"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row v-if="devices.editForm.apCount - 0 > 4">
          <el-col :md="12" :sm="24">
            <el-form-item label="AP05型号">
              <el-input v-model="devices.editForm.ap_5_model"></el-input>
            </el-form-item>
          </el-col>
          <el-col :md="12" :sm="24">
            <el-form-item label="AP05序列号">
              <el-input v-model="devices.editForm.ap_5_serial"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="devices.editVisible = false">取 消</el-button>
        <el-button type="primary" @click="editDevices">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
var app0;
export default {
  data() {
    return {
      formInline: {
        stores: ""
      },
      result: [],
      StoreInfo: "",
      checkLoading: false,
      activeName: "check",
      contactTable: [],
      devicesTable: [],
      contact: {
        keywords: "",
        addForm: {
          storeNO: "",
          region: "",
          telephone: "",
          regional_manager: "",
          regional_manager_phone: "",
          regional_it: "",
          regional_it_phone: ""
        },
        addRules: {
          storeNO: { required: true, message: "请输入店铺号", trigger: "blur" },
          telephone: {
            required: true,
            message: "请输入电话号码",
            trigger: "blur"
          },
          regional_it: {
            required: true,
            message: "请输入区域IT",
            trigger: "blur"
          },
          regional_it_phone: {
            required: true,
            message: "请输入IT电话",
            trigger: "blur"
          }
        },
        CurrPage: 1,
        PageSize: 10,
        Total: 0,
        addVisible: false,
        loading:false
      },
      devices: {
        keywords: "",
        addForm: {
          apCount: 1,
          ap_1: "",
          ap_1_ip: "",
          ap_1_model: "",
          ap_1_serial: "",
          ap_1_version: "",
          ap_2: "",
          ap_2_ip: "",
          ap_2_model: "",
          ap_2_serial: "",
          ap_2_version: "",
          ap_3: "",
          ap_3_ip: "",
          ap_3_model: "",
          ap_3_serial: "",
          ap_3_version: "",
          ap_4: "",
          ap_4_ip: "",
          ap_4_model: "",
          ap_4_serial: "",
          ap_4_version: "",
          ap_5: "",
          ap_5_ip: "",
          ap_5_model: "",
          ap_5_serial: "",
          ap_5_version: "",
          is_aruba: "",
          router: "",
          router_ip: "",
          storeNO: ""
        },
        editForm: {
          apCount: 0,
          ap_1: "",
          ap_1_ip: "",
          ap_1_model: "",
          ap_1_serial: "",
          ap_1_version: "",
          ap_2: "",
          ap_2_ip: "",
          ap_2_model: "",
          ap_2_serial: "",
          ap_2_version: "",
          ap_3: "",
          ap_3_ip: "",
          ap_3_model: "",
          ap_3_serial: "",
          ap_3_version: "",
          ap_4: "",
          ap_4_ip: "",
          ap_4_model: "",
          ap_4_serial: "",
          ap_4_version: "",
          ap_5: "",
          ap_5_ip: "",
          ap_5_model: "",
          ap_5_serial: "",
          ap_5_version: "",
          is_aruba: "",
          router: "",
          router_ip: "",
          storeNO: ""
        },
        addRules: {
          storeNO: { required: true, message: "请输入店铺号", trigger: "blur" },
          router_ip: {
            required: true,
            message: "请输入IP地址",
            trigger: "blur"
          },
          router: {
            required: true,
            message: "请输入门店型号",
            trigger: "blur"
          }
        },
        CurrPage: 1,
        PageSize: 10,
        Total: 0,
        loading:false,
        addVisible: false,
        editVisible: false
      }
    };
  },
  methods: {
    showEditDevices(row) {
      this.devices.editForm = { ...this.devices.editForm, ...row };
      for (var key in row) {
        /^ap_\d$/.test(key) && row[key]
          ? (this.devices.editForm.apCount += 1)
          : "";
      }
      this.devices.editVisible = true;
    },
    async deleteDevices(storeNO) {
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
        url: "/cmdb/devices/" + storeNO,
        method: "delete"
      }).then(res => {
        this.devicesTable = res.data;
        this.devices.Total = res.data.length;
      });
    },
    addDevices() {
      this.$refs.addDeviceRef.validate(async valid => {
        if (!valid) return;
        await this.$request({
          url: "/cmdb/devices/",
          method: "post",
          data: this.devices.addForm
        }).then(res => {
          this.devicesTable = res.data;
          this.devices.Total = res.data.length;
          this.devices.CurrPage = 1;
          this.devices.addVisible = false;
        });
      });
    },
    editDevices() {
      this.$request({
        url: "/cmdb/devices/" + this.devices.editForm.storeNO,
        method: "put",
        data: this.devices.editForm
      }).then(res => {
        this.devicesTable = res.data
        this.$message.success("更新数据成功！");
      });
      this.devices.editVisible = false;
    },
    // 监听添加对话框关闭
    diglogClose(event) {
      if (event === "addContact") {
        this.$refs.addContactRef.resetFields();
        this.contact.addForm.regional_manager = "";
        this.contact.addForm.regional_manager_phone = "";
      } else if (event === "addDevice") {
        this.$refs.addDeviceRef.resetFields();
        this.devices.addForm = {
          apCount: 1,
          ap_1: "",
          ap_1_ip: "",
          ap_1_model: "",
          ap_1_serial: "",
          ap_1_version: "",
          ap_2: "",
          ap_2_ip: "",
          ap_2_model: "",
          ap_2_serial: "",
          ap_2_version: "",
          ap_3: "",
          ap_3_ip: "",
          ap_3_model: "",
          ap_3_serial: "",
          ap_3_version: "",
          ap_4: "",
          ap_4_ip: "",
          ap_4_model: "",
          ap_4_serial: "",
          ap_4_version: "",
          ap_5: "",
          ap_5_ip: "",
          ap_5_model: "",
          ap_5_serial: "",
          ap_5_version: "",
          is_aruba: "",
          router: "",
          router_ip: "",
          storeNO: ""
        };
      } else if (event === "editDevice") {
        this.$refs.editDeviceRef.resetFields();
        this.devices.editForm = {
          apCount: 0,
          ap_1: "",
          ap_1_ip: "",
          ap_1_model: "",
          ap_1_serial: "",
          ap_1_version: "",
          ap_2: "",
          ap_2_ip: "",
          ap_2_model: "",
          ap_2_serial: "",
          ap_2_version: "",
          ap_3: "",
          ap_3_ip: "",
          ap_3_model: "",
          ap_3_serial: "",
          ap_3_version: "",
          ap_4: "",
          ap_4_ip: "",
          ap_4_model: "",
          ap_4_serial: "",
          ap_4_version: "",
          ap_5: "",
          ap_5_ip: "",
          ap_5_model: "",
          ap_5_serial: "",
          ap_5_version: "",
          is_aruba: "",
          router: "",
          router_ip: "",
          storeNO: ""
        };
      }
    },
    // 添加对话框确定事件
    addContact() {
      this.$refs.addContactRef.validate(async valid => {
        if (!valid) return;
        await this.$request({
          url: "/cmdb/contacts/",
          method: "post",
          data: this.contact.addForm
        })
          .then(res => {
            // 对后端数据加上isSet，以控制编辑输入框的显示
            res.data.map(i => {
              i.isSet = false;
              return i;
            });
            this.contactTable = res.data;
            this.contact.Total = res.data.length;
            this.contact.CurrPage = 1;
            this.contact.addVisible = false;
          })
          .catch(err => {
            this.$message.error("添加店铺联系信息失败！");
            this.contact.addVisible = false;
          });
      });
    },
    ContactUpdate(row, index, cg) {
      //点击修改，判断是否已经保存所有操作
      for (let i of this.contactTable) {
        if (i.isSet && i.storeNO != row.storeNO) {
          return this.$message.warning("请先保存当前项");
        }
      }
      // 是否取消操作
      if (cg) {
        if (row.isSet) {
          var form = {
            telephone: row.telephone,
            regional_manager: row.regional_manager,
            regional_manager_phone: row.regional_manager_phone,
            regional_it: row.regional_it,
            regional_it_phone: row.regional_it_phone,
            region: row.region
          };
          this.$request({
            url: "/cmdb/contacts/" + row.storeNO,
            method: "put",
            data: form
          }).then(res => {
            this.contactTable = res.data.map(i => {
              i.isSet = false;
              return i;
            });
            this.$message.success("更新数据成功！");
          });
        } else {
          row.isSet = true;
        }
      } else {
        // if (!app.master_user.sel.id) app.master_user.data.splice(index, 1);
        row.isSet = false;
      }
    },
    async ContactDelete(storeNO) {
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
        url: "/cmdb/contacts/" + storeNO,
        method: "delete"
      }).then(res => {
        this.contactTable = res.data.map(i => {
          i.isSet = false;
          return i;
        });
        this.contact.Total = res.data.length;
      });
    },
    contactSizeChange(val) {
      this.contact.PageSize = val;
    },
    contactCurrentChange(val) {
      this.contact.CurrPage = val;
    },
    deviceSizeChange(val) {
      this.devices.PageSize = val;
    },
    deviceCurrentChange(val) {
      this.devices.CurrPage = val;
    },
    async getDevicesList() {
      this.devices.loading=true
      await this.$request({
        url: "/cmdb/devices/" + this.devices.keywords,
        method: "get"
      })
        .then(res => {
          this.devicesTable = res.data;
          console.log(this.devicesTable)
          this.devices.Total = res.data.length;
          this.devices.CurrPage = 1;
          this.devices.loading=false
        })
        .catch(err => {
          this.$message.error("获取设备信息表失败！");
          this.devices.loading=false
        });
    },
    async getContactList() {
      this.contact.loading=true
      await this.$request({
        url: "/cmdb/contacts/" + this.contact.keywords,
        method: "get"
      })
        .then(res => {
          res.data.map(i => {
            i.isSet = false;
            return i;
          });
          this.contactTable = res.data;
          this.contact.Total = res.data.length;
          this.contact.CurrPage = 1;
          this.contact.loading=false
        })
        .catch(err => {
          this.$message.error("获取联系电话表失败！");
          this.contact.loading=false
        });
    },
    async tabActiveClick() {
      if (this.activeName === "contact") {
        this.getContactList();
      } else if (this.activeName === "device") {
        this.getDevicesList();
      }
    },
    async onCheck() {
      if (!/^\d+$/.test(this.formInline.stores)) {
        this.formInline.stores = "";
        return this.$message.error("请输入正确的店铺号！");
      }
      this.checkLoading = true;
      this.$request({
        url: "/api/Info_Refer/",
        method: "post",
        data: this.formInline
      }).then(res => {
        res.data["ap"] = {};
        for (var key in res.data) {
          if (!/AP\d\d/.test(key)) {
            continue;
          }
          if (res.data[key]) {
            var valueList = Object.values(res.data[key]);
            if (valueList[0] !== "" || valueList[1] !== "") {
              res.data["ap"][key.toUpperCase()] = valueList;
            }
          }
        }
        res.data["ap_count"] = Object.keys(res.data["ap"]).length;
        this.StoreInfo = res.data;
      });
      await this.$request({
        url: "/api/Cisco_data/",
        method: "post",
        data: this.formInline
      })
        .then(res => {
          console.log(res)
          this.result = res.data;
          this.checkLoading = false;
        })
        .catch(err => {
          this.result = [];
          this.checkLoading = false;
        });
    }
  },
  beforeCreate() {
    app0 = this;
  },
  filters: {
    //过滤触发hover提示框的内容
    checkStatusContent(val) {
      // console.log(val);
      if (val.status) {
        return val.status;
      } else if (val.length < 15) {
        return val;
      } else {
        return "Detail";
      }
    },
    checkLabelContent(label) {
      var regRes = /AP\d\d/g.exec(label);
      if (regRes === null) {
        return label;
      }
      // console.log(Object.keys(app0.StoreInfo.ap));
      // console.log(regRes[0]);
      if (Object.keys(app0.StoreInfo.ap).indexOf(regRes[0]) > -1) {
        return label;
      } else {
        return label + "<span style='color:orangered'>(规划)</span>";
      }
    },
    //过滤hover提示框的内容
    ExpandContent(val) {
      var reg = new RegExp("\r\n", "g");
      if (val.data) {
        var str = "";
        for (var key in val.data) {
          str +=
            key.toUpperCase() + "：" + val.data[key].toUpperCase() + "<br/>";
          // console.log(str)
        }
        return str;
      } else if (val.vlan) {
        val.vlan = val.vlan.replace(reg, "<br/>");
        val.survey = val.survey.replace(reg, "<br/>");
        var str = val.survey + val.vlan;
        return str;
      } else {
        if (reg.test(val)) {
          val = val.replace(reg, "<br/>");
        }
        return val;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.input-mr-10{
  margin-right: 10px;
}
.check-group {
  margin-top: 20px;
  // border: 1px solid #eee;
  & > p {
    border-bottom: 2px dotted #eee;
    padding-bottom: 10px;
  }
  .check-result {
    display: flex;
    flex-direction: column;
    p {
      display: flex;
      margin: 5px;
      flex-direction: row;
      justify-content: space-around;
      .left {
        width: 100px;
      }
      .center {
        color: greenyellow;
        letter-spacing: 20px;
        width: 200px;
      }
    }
  }
}
.info-group {
  margin-top: 20px;
  & > p {
    border-bottom: 2px dotted #eee;
    padding-bottom: 10px;
  }
  .info {
    border-right: 1px solid #d0cfcf;
    border-bottom: 1px solid #d0cfcf;
    td {
      border-left: 1px solid #d0cfcf;
      border-top: 1px solid #d0cfcf;
      padding: 5px;
    }
  }
}
@media (max-width: 768px) {
  .info {
    padding-left: 0;
  }
}
.el-table {
  margin-top: 10px;
}
</style>
