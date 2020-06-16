<template>
  <el-main>
    <el-row>
      <el-col :xs="24" :sm="24" :lg="5" class="status-group">
        <el-col :xs="24" :sm="24" :lg="11">
          <p>状态</p>
          <div class="nums">66</div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="11">
          <p>状态</p>
          <div class="nums">66</div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="11">
          <p>状态</p>
          <div class="nums">66</div>
        </el-col>
        <el-col :xs="24" :sm="24" :lg="11">
          <p>状态</p>
          <div class="nums">66</div>
        </el-col>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="11" class="p-center">
        <p>MTL VPN Connected Users名单</p>
        <el-table :data="tableData" max-height="300px">
          <el-table-column prop="time" label="日期" width="180"></el-table-column>
          <el-table-column prop="name" label="姓名" width="180"></el-table-column>
          <el-table-column prop="device" label="设备" width="180"></el-table-column>
          <el-table-column prop="status" label="状态" width="180"></el-table-column>
        </el-table>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8" class="p-center">
        <vline :id="'chart1'" :title="'MTLCN FSIDC to MTLHK SLA Monitoring'" :idDict="[{'name': 'FSIDCToHK(GRE)', 'id':53064}]"></vline>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :sm="24" :lg="12" class="p-center">
        <vline :id="'chart2'" :title="'DAMA Internet sla监控情况'" :idDict="[{'name': 'WeWorkToFSIDC', 'id':53063},{'name': 'WeWorkToPubliceDNS', 'id':53062},{'name': 'WeWorkToBJIDCFTTB(GW)', 'id':53302},{'name': 'WeWorkToBJIDCASR', 'id':53303},{'name': 'WeWorkToBJIDCWetchat', 'id':53304},{'name': 'WeWorkToFSIDCASR', 'id':53305}]"></vline>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="12" class="p-center">
        <vline :id="'chart3'" :title="'MTLCN FSIDC to MTLHK SLA Monitoring'" :idDict="[{'name': 'FSIDCToGZ', 'id':53067},{'name': 'FSIDCToSH', 'id':53068},{'name': 'FSIDCToBJ', 'id':53069},{'name': 'FSIDCToPY', 'id':53071}]"></vline>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :sm="24" :lg="12" class="p-center">
        <v-speedLine :id="'chart4'" :title="'DAMA Internet出口流量情况'" :idDict="[{'name': 'CONNECT_TO_CT_Traffic', 'id':33080},{'name': 'CONNECT_TO_CU_Traffic', 'id':33108}]"></v-speedLine>

      </el-col>
      <el-col :xs="24" :sm="24" :lg="12" class="p-center">
        <v-speedLine :id="'chart5'" :title="'MTLCN-HK CPCNet 10M MPLS - MTLHK'" :idDict="[{'name': 'Gi0/0/2 CPCNet10M MPLS-MTLHK', 'id':10832}]"></v-speedLine>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :sm="24" :lg="12" class="p-center">
        <v-speedLine :id="'chart6'" :title="'佛山IDC_ 出口流量情况(20M)'" :idDict="[{'name': 'INTERNET_20M', 'id':53713}]"></v-speedLine>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="12" class="p-center">
        <v-sankey :id="'chart7'"  :title="'佛山店铺出口-NetFlow Analyzer流量监控'"></v-sankey>
      </el-col>
    </el-row>
  </el-main>
</template>

<script>
import line from "@/components/echarts/line";
import Sankey from "@/components/echarts/Sankey";
import speedLine from "@/components/echarts/speedLine";

export default {
  data: function() {
    return {
      tableData: []
    };
  },
  created() {
    this.getTable();
  },
  methods: {
    getTable() {
      this.$request({
        url: "/api/getMTLvpnUser",
        method: "get"
      }).then(res => {
        this.tableData = res.data;
      });
    }
  },
  components: {
    vline: line,
    "v-speedLine": speedLine,
    "v-sankey": Sankey,
  }
};
</script>

<style lang="scss" scoped>
.el-row {
  margin-bottom: 10px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.status-group {
  padding: 0 !important;
  // display: flex;
  // justify-content: space-between;
  // flex-wrap: wrap;
  .el-col {
    // width: 44%;
    // margin-left: 1rem;
    background: #26bff4;
    // margin-bottom: 1rem;
    text-align: center;
    color: #fff;
    margin-right: 5px;
    margin-bottom: 5px;
    p {
      line-height: 30px;
      height: 30px;
    }
    .nums {
      padding: 32px 0;
      font-size: 36px;
    }
  }
}
.p-center {
  text-align: center;
  p {
    line-height: 20px;
    height: 20px;
  }
}
</style>
