<template>
  <div class="main">
    <div class="status-group">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="grid-content bg-purple" />
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple" />
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple" />
        </el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple" />
        </el-col>
      </el-row>
    </div>
    <ve-line :data="chartData" />
  </div>
</template>

<script>
import { timeComputed } from "@/utils/validate";
export default {
  data: function() {
    return {
      chartData: {
        columns: [],
        rows: [
          // { '日期': '1/5', '访问用户': 3792, '下单用户': 3492, '下单率': 0.323 },
          // { '日期': '1/6', '访问用户': 4593, '下单用户': 4293, '下单率': 0.78 }
        ]
      }
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      var dateTime = timeComputed(60);
      console.log(dateTime);
      this.$axios({
        //   url:'/api/getHistoryFromPRTG/?custom=1&=2020-03-28-08-59-33&edate=2020-03-28-09-59-33&idDict=[{"name":"沙河","id":"10"},]',
        // }).then(res => {
        method: "POST",
        url: "/api/getHistoryFromPRTG/",
        data: JSON.stringify({
          custom: "0",
          sdate: dateTime[0],
          edate: dateTime[1],
          idDict: [
            { name: "佛山IDC至香港", id: "53311" },
            { name: "GZIDC", id: "8633" }
          ]
        }),
        headers: {
          "Content-Type": "application/json;"
        }
        // async : false,
      }).then(res => {
        console.log(res.data);
        this.chartData.rows = res.data;
        this.chartData.columns = ["date", "佛山IDC至香港", "GZIDC"];
        // console.log(this.chartData)
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 64px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>
