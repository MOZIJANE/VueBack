<template>
  <div />
</template>

<script>
import { timeComputed } from "@/utils/validate";
import resize from './mixins/resize'
// import  'echarts/theme/shine'
// import  'echarts/theme/green'  //不错
// import  'echarts/theme/bee-inspired'
// import  'echarts/theme/azul'  //还好
// import  'echarts/theme/blue'   //不错
// import  'echarts/theme/dark-bold'  //不错
// import  'echarts/theme/helianthus'  //不错
// import  'echarts/theme/dark-bold'  //不错

export default {
  mixins: [resize],
  props: {
    timeLine: {
      type: Number,
      default: 60
    },
    idDict: {
      type: Array,
      default: () => {}
    }
  },

  watch: {
    x: {
      handler(newVal, oldVal) {
        // console.log("tag", newVal);
        // console.log("oldVal: ", oldVal);
        this.timer();
      },
      deep: true //对象内部属性的监听，关键。
    }
  },
  data() {
    return {
      chart: null,
      x: 0, //watch监听chartData有问题，因此用x
      chartData: {},
      option: {
        // title: {
        //   text: this.title,
        //   x: "center",
        //   textStyle: {
        //     fontSize: 17,
        //     color: "#000",
        //     fontWeight: "normal"
        //   }
        // },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985"
            }
          },
          formatter: function(params, ticket, callback) {
            //图表title名称
            var seriesName = params[0].seriesName;
            //值
            var value = params[0].value;
            // console.log(typeof value)
            var valueFliter = (value, index) => {
              return `${value[0].replace("T", " ")}  ${value[1]}ms`;
            };
            return seriesName + "<br />" + valueFliter(value);
          }
        },
        legend: {
          //图例组件，颜色和名字
          right: "10%",
          top: "10%",
          itemGap: 16,
          itemWidth: 18,
          itemHeight: 10,
          data: "",
          //icon:'image://../wwwroot/js/url2.png', //路径
          textStyle: {
            // color: "#a8aab0",
            fontStyle: "normal",
            fontFamily: "微软雅黑",
            fontSize: 12
          }
        },
        xAxis: {
          name: "时间",
          type: "time",
          splitLine: {
            show: false
          }
        },
        yAxis: {
          name: "延迟",
          type: "value",
          boundaryGap: [0, "100%"],
          splitLine: {
            show: true
          }
        },
        series: []
      },
      themeObj:{
        "black":"dark-bold",
        "dl":"green",
        "violet":"green"
      }
    };
  },
  created() {
    this.getData();
  },
  mounted() {},
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart() {
      if (this.chart) {
        this.chart.setOption(this.option);
      } else {
        var theme=this.$store.state.theme.activeName
        this.chart = this.$echarts.init(this.$el,this.themeObj[theme]);

        this.chart.setOption(this.option);
      }
    },
    getData() {
      var dateTime = timeComputed(this.timeLine);
      // console.log(this.idDict);
      this.x += 1;
      this.$request({
        url: "/api/getHistoryFromPRTG/",
        method: "post",
        data: {
          custom: "0",
          // sdate: dateTime[0],
          sdate: dateTime[0],
          edate: dateTime[1],
          idDict: this.idDict
        }
      }).then(res => {
        if (res.data) {
          this.option.series = [];
          // console.log(res.data)
          for (var ke in res.data) {
            var line = {
              name: "",
              type: "line",
              showSymbol: false,
              // stack: 100,
              // step: true,
              data: "",
              areaStyle: {
                // normal: {
                //   // "color": "#d4f8e8" //改变区域颜色
                //   color: "#D1E4CB",
                //   // opacity: 0.9
                // }
              },
              itemStyle: {
                // normal: {
                //   color: "#99C28B",
                  lineStyle: {
                    // 系列级个性化折线样式
                    // width: 0.7,
                    type: "solid"
                  }
                // }
              }
            };
            line.name = ke;
            // console.log(line.name)
            // console.log(this.series[i])
            this.chartData[ke] = res.data[ke];
            // console.log(this.chartData[ke])
            line.data = this.chartData[ke];
            // console.log(series[i])
            this.option.series.push(line);
          }
        }
        this.initChart();
      });
    },
    timer() {
      return setTimeout(() => {
        this.getData();
      }, 60 * 5 * 1000);
    }
  },
  destroyed() {
    clearTimeout(this.timer);
  }
};
</script>
<style lang="scss" scoped>
  @media (max-width: 768px) {
    div{
      width:100%;
      height: 16.4rem;
    }
  }
  @media (min-width: 992px) {
    div{
      width:100%;
      height: 20.4rem;
    }
  }
</style>