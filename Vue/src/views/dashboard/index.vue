<template>
  <el-main>
    <el-row>
      <el-col :xs="24" :md="5">
        <div
          class="lates"
          v-loading="loading"
          element-loading-spinner="el-icon-loading"
          element-loading-custom-class="mask"
        >
          <div class="title">国内各办公室链路延时</div>
          <ul class="lates-list">
            <li v-for="(item, index) in latesObj.office" :key="index">
              <span class="left">{{ item.name }}</span
              ><span class="right">{{ item.value }} ms</span>
            </li>
          </ul>
        </div>
      </el-col>
      <el-col :xs="24" :md="7" class="p-center">
        <el-card
          shadow="never"
          v-loading="loading"
          element-loading-spinner="el-icon-loading"
          element-loading-custom-class="mask"
          class="unit-per"
        >
          <div class="title">国内各区域办公室互联链路流量</div>
          <ul>
            <li v-for="(item, index) in unitPerObj.office" :key="index">
              <p class="label">{{ item.name }}</p>
              <p class="prog">
                <el-progress
                  :percentage="item.value"
                  :stroke-width="10"
                  color="#5BC0DE"
                ></el-progress>
              </p>
            </li>
          </ul>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="7" class="p-center">
        <el-card
          shadow="never"
          v-loading="loading"
          element-loading-spinner="el-icon-loading"
          element-loading-custom-class="mask"
          class="unit-per"
        >
          <div class="title">各区域办公室&IDC Internet 出口流量</div>
          <ul>
            <li v-for="(item, index) in unitPerObj.internal" :key="index">
              <p class="label">{{ item.name }}</p>
              <p class="prog">
                <el-progress
                  :percentage="item.value"
                  :stroke-width="10"
                  color="#5BC0DE"
                ></el-progress>
              </p>
            </li>
          </ul>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="5">
        <div
          class="lates"
          v-loading="loading"
          element-loading-spinner="el-icon-loading"
          element-loading-custom-class="mask"
        >
          <div class="title">办公室Internet延时</div>
          <ul class="lates-list">
            <li v-for="(item, index) in latesObj.internal" :key="index">
              <span class="left">{{ item.name }}</span
              ><span class="right">{{ item.value }} ms</span>
            </li>
          </ul>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">GZ To HK Netflow analyzer TOP 10</div>
          <topbar :idDict="[{ id: '61236' }]"></topbar
        ></el-card>
      </el-col>
      <el-col :xs="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">HK To GZ Netflow analyzer TOP 10</div>
          <topbar :idDict="[{ id: '61235' }]"></topbar
        ></el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">MTSH To FSIDC Netflow TOP 10</div>
          <topbar :idDict="[{ id: '61299' }]"></topbar
        ></el-card>
      </el-col>
      <el-col :xs="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">MSZ To FSIDC Netflow TOP 10</div>
          <topbar :idDict="[{ id: '61304' }]"></topbar
        ></el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :sm="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">HK To GZ Netflow analyzer</div>
          <sankey :apiName="'/api/getSankeyFromUrl_HK_GZ/'"></sankey>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">GZ To HK Netflow analyzer</div>
          <sankey></sankey>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :sm="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">DAMA To INTERNET BW:20M (CT)</div>
          <speed-line
            :idDict="[{ name: 'CONNECT_TO_CT_Traffic', id: 33080 }]"
          ></speed-line>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">DAMA To INTERNET BW:100M (CU)</div>
          <speed-line
            :idDict="[{ name: 'CONNECT_TO_CU_Traffic', id: 33108 }]"
          ></speed-line>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :sm="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">FSIDC To INTERNET BW:20M</div>
          <speed-line
            :idDict="[{ name: 'Gi1/0/45 INTERNET_20M', id: 53713 }]"
          ></speed-line>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">DAMA To PY Office BW:20M (CMCC)</div>
          <speed-line
            :idDict="[{ name: 'CMCCToPANYUOffice(20M)', id: 53057 }]"
          ></speed-line>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :sm="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">MTLFSIDC To HK HGC BW:20M</div>
          <speed-line
            :idDict="[{ name: 'FSIDC To HK BW:20M', id: 61372 }]"
          ></speed-line>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" class="p-center">
        <el-card shadow="hover">
          <div class="title">MTL TO Customer SLA Monitoring</div>
          <vline
            :idDict="[
              { name: 'MTL TO ASWI', id: 17321 },
              { name: 'MTL TO WTCCN(Backup)', id: 58256 }
            ]"
          ></vline>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :sm="24" :md="24" class="p-center">
        <el-card shadow="hover">
          <div class="title">MTLCN FSIDC to MTLHK SLA Monitoring</div>
          <vline
            :timeLine="240"
            :idDict="[{ name: 'FSIDCToHK(GRE)', id: 53064 },{ name: 'FSIDCToHK', id: 61373 }]"
          ></vline>
        </el-card>
      </el-col>
    </el-row>
  </el-main>
</template>

<script>
import { timeComputed } from "@/utils/validate";
import line from "@/components/echarts/line";
import speedLine from "@/components/echarts/speedLine";
import sankey from "@/components/echarts/sankey";
import topbar from "@/components/echarts/topbar";

export default {
  data: function() {
    return {
      tableData: [],
      latesObj: {
        office: [],
        internal: []
      },
      loading: true,
      i: 0,
      unitPerObj: {
        office: [],
        internal: []
      }
    };
  },
  created() {
    this.getLates();
    this.getUnitPer();
  },
  methods: {
    // 获取流量百分比
    getUnitPer() {
      this.unitPerObj = { office: [], internal: [] };
      var dateTime = timeComputed(20);
      var idDict = [
        { id: 53734 },
        { id: 53733 },
        { id: 53057 },
        { id: 33080 },
        { id: 33108 },
        { id: 33242 },
        { id: 53713 }
      ];
      this.$request({
        url: "/api/getNow_data_fromPRTG/",
        method: "post",
        data: {
          custom: "0",
          // sdate: dateTime[0],
          sdate: dateTime[0],
          edate: dateTime[1],
          idDict: idDict
        }
      }).then(res => {
        var data = res.data;
        for (var key in data) {
          if (key.indexOf("053") > -1) {
            this.unitPerObj.office.push({
              name: "MSTP_FSIDC To SZOffice(2M)",
              value: data[key]
            });
          } else if (key.indexOf("112") > -1) {
            this.unitPerObj.office.push({
              name: "MSTP_FSIDC To SZOffice(4M)",
              value: data[key]
            });
          } else if (key.indexOf("10124") > -1) {
            this.unitPerObj.office.push({
              name: "CMCC To PYOffice",
              value: data[key]
            });
          } else if (key.indexOf("10623") > -1) {
            this.unitPerObj.internal.push({
              name: "DAMA To INTERNET BW:100M(CU)",
              value: data[key]
            });
          } else if (key.indexOf("(003) outside") > -1) {
            this.unitPerObj.internal.push({
              name: "PANYU To INTERNET BW:100M",
              value: data[key]
            });
          } else if (key.indexOf("(052) Gi1") > -1) {
            this.unitPerObj.internal.push({
              name: "FSIDC To INTERNET BW:20M",
              value: data[key]
            });
          } else if (key.indexOf("(052) Gi1") > -1) {
            this.unitPerObj.internal.push({
              name: "FSIDC To INTERNET BW:20M",
              value: data[key]
            });
          } else {
            this.unitPerObj.office.push({
              name: "DAMA To INTERNET(CT)",
              value: data[key]
            });
          }
        }
        this.unitPerObj.office.sort(this.sortKey("value"));
      });
    },
    //获取延时
    getLates() {
      this.latesObj = { office: [], internal: [] };
      var dateTime = timeComputed(20);
      var idDict = [
        { name: "BJInternet", id: 60139 },
        { name: "SHInternet", id: 60138 },
        { name: "SZInternet", id: 60137 },
        { name: "FSIDCGZOFFICE", id: 53067 },
        { name: "FSIDCSHOFFICE", id: 53068 },
        { name: "FSIDCBJOFFICE", id: 53069 },
        { name: "FSIDCSZOFFICE", id: 53070 },
        { name: "FSIDCPANYU", id: 53071 },
        { name: "FSIDCDONGGUAN", id: 61334 }
      ];
      this.$request({
        url: "/api/getHistoryFromPRTG/",
        method: "post",
        data: {
          custom: "0",
          // sdate: dateTime[0],
          sdate: dateTime[0],
          edate: dateTime[1],
          idDict: idDict
        }
      }).then(res => {
        var data = res.data;
        for (var key in data) {
          // 延时
          let lastLate = data[key][data[key].length - 1][1];
          lastLate = lastLate ? lastLate : 1;
          if (key.indexOf("BJInternet") > -1) {
            this.latesObj.internal.push({
              name: "BJ To Internet",
              value: lastLate
            });
          } else if (key.indexOf("SHInternet") > -1) {
            this.latesObj.internal.push({
              name: "SH To Internet",
              value: lastLate
            });
          } else if (key.indexOf("SZInternet") > -1) {
            this.latesObj.internal.push({
              name: "SZ To Internet",
              value: lastLate
            });
          } else if (key.indexOf("FSIDCGZOFFICE") > -1) {
            this.latesObj.office.push({
              name: "FSIDC To GZOFFICE",
              value: lastLate
            });
          } else if (key.indexOf("FSIDCSHOFFICE") > -1) {
            this.latesObj.office.push({
              name: "FSIDC To SHOFFICE",
              value: lastLate
            });
          } else if (key.indexOf("FSIDCBJOFFICE") > -1) {
            this.latesObj.office.push({
              name: "FSIDC To BJOFFICE",
              value: lastLate
            });
          } else if (key.indexOf("FSIDCSZOFFICE") > -1) {
            this.latesObj.office.push({
              name: "FSIDC To SZOFFICE",
              value: lastLate
            });
          } else if (key.indexOf("FSIDCPANYU") > -1) {
            this.latesObj.office.push({
              name: "FSIDC To PANYU",
              value: lastLate
            });
          } else if (key.indexOf("FSIDCDONGGUAN") > -1) {
            this.latesObj.office.push({
              name: "FSIDC To DONGGUAN",
              value: lastLate
            });
          }
        }
        this.latesObj.internal.sort(this.sortKey("value"));
        this.latesObj.office.sort(this.sortKey("value"));
        this.i += 1;
        this.loading = false;
      });
    },
    timer() {
      return setTimeout(() => {
        this.loading = true;
        // console.log("1111", this.loading);
        this.getLates();
        this.getUnitPer();
      }, 5 * 60 * 1000);
    },
    // 排序方法
    sortKey(key) {
      return function(val1, val2) {
        return val2[key] - val1[key];
      };
    }
  },
  watch: {
    i: {
      handler(newVal, oldVal) {
        // console.log("newVal", newVal);
        this.timer();
      },
      deep: true //对象内部属性的监听，关键。
    }
  },
  destroyed() {
    clearTimeout(this.timer);
  },
  components: {
    vline: line,
    "speed-line": speedLine,
    sankey,
    topbar
  }
};
</script>

<style lang="scss" scoped>
.lates {
  background: rgb(38, 185, 154);
  color: #fff;
  padding: 10px;
  .title {
    font-size: 20px;
  }
  .lates-list {
    display: flex;
    list-style: none;
    justify-content: space-between;
    padding: 0;
    flex-direction: column;
    height: 290px;
    li {
      display: flex;
      justify-content: space-between;
      padding: 12px 0;
      border-bottom: 2px solid #eee;
      .left {
        font-size: 16px;
      }
      .right {
        font-size: 20px;
        font-weight: 600;
      }
    }
  }
}
/deep/ .el-card__body {
  padding: 5px;
}

.p-center {
  .title {
    color: #73879c;
    border-bottom: 2px solid #e6e9ed;
    padding: 5px 0;
    text-align: left;
    font-family: Arial, Helvetica, sans-serif;
  }
}
@media (min-width: 992px) {
  .title-row {
    // & > .el-col:first-child,& > .el-col:nth-child(2) {
    //   margin-right: 10px;
    // }
  }
  .title-count .status:first-child:before {
    border-left: 0;
  }
  .title-count .status:nth-child(4):before {
    border-left: 0;
  }
  .el-card {
    margin-right: 5px;
  }
  .el-row {
    margin-bottom: 10px;
  }
  .lates{
    margin-right: 5px;
  }
  .p-center {
    .title {
      font-size: 20px;
      line-height: 29px;
    }
  }
}
@media (max-width: 768px) {
  .title-count .status {
    border-bottom: 1px solid #d9dee4;
  }
  .title-row {
    & > .el-col:first-child {
      margin-bottom: 5px;
    }
  }
  .el-table {
    margin-bottom: 5px;
  }
  .el-card {
    margin-right: 0;
  }
  .p-center {
    margin-bottom: 5px;
  }
  .lates{
    margin-bottom: 5px;
  }
  .p-center {
    .title {
      font-size: 17px;
      line-height: 20px;
    }
  }
}
.unit-per {
  ul {
    // margin:0;
    display: flex;
    list-style: none;
    justify-content: space-between;
    padding: 0;
    flex-direction: column;
    height: 280px;
    margin-left: 10px;
  }
  li {
    list-style: none;
    margin: 8px 0;
  }
  p {
    margin: 4px 0;
    font-size: 15px;
    color: #7f91a5;
    font-family: Arial, Helvetica, sans-serif;
  }
  .prog {
    width: 75%;
  }
}
</style>
