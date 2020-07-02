<template>
  <div />
</template>

<script>
import { timeComputed } from "@/utils/validate";
import resize from "./mixins/resize";


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
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985"
            }
          },
          formatter:(params, ticket, callback)=>{
            var str = "";
            params.forEach((value, index) => {
              var seriesName = params[index].seriesName;
              // console.log(params[index].value[1]);
              var value = this.flowTrun(params[index].value[1]);
              str += seriesName + ": " + value + "<br />";
            });
            return str;
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
            show: true
          }
        },
        yAxis: {
          name: "流量",
          type: "value",
          boundaryGap: [0, "100%"],
          splitLine: {
            show: true
          },
          axisLabel: {
            formatter: (value, index) => {
              var value = this.flowTrun(value);
              return value;
            }
          }
        },
        series: []
      },
      themeObj:{
        "black":"dark-bold",
        "dl":"westeros",
        "violet":"westeros"
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
      // this.chart.setOption({backgroundColor: this.getTheme.bg});
      window.addEventListener("resize", this.chart.resize);
      // EleResize.on(this.chart, listener)
    },
    getData() {
      var dateTime = timeComputed(this.timeLine);
      // console.log(this.idDict);
      this.x += 1;
      // console.log()
      this.$request({
        url: "/api/getHistory_speed_FromPRTG/",
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
          // var colorList = [
          //   "rgba(38, 185, 154, 0.38)",
          //   "rgba(3, 88, 106, 0.38)"
          // ];
          var colorIndex = 0;
          // console.log(res.data)
          for (var ke in res.data) {
            var line = {
              name: "",
              type: "line",
              showSymbol: false,
              hoverAnimation: false,
              data: "",
              // stack: 100,
              smooth: true,
              areaStyle: {
                // normal: {
                //   // "color": "#d4f8e8" //改变区域颜色
                //   color: colorList[colorIndex]
                //   // opacity: 0.9
                // }
              },
              itemStyle: {
                normal: {
              //     color: colorList[colorIndex],
                  lineStyle: {
                    // 系列级个性化折线样式
                    width: 0.7,
                    type: "solid"
                  }
                }
              }
            };
            // console.log(colorList[colorIndex]);
            line.name = ke;
            // console.log(line.name)
            // console.log(this.series[i])
            this.chartData[ke] = res.data[ke];
            // console.log(this.chartData[ke])
            line.data = this.chartData[ke];
            // console.log(series[i])
            this.option.series.push(line);
            colorIndex += 1;
          }
        }
        this.initChart();
      });
    },
    timer() {
      return setTimeout(() => {
        this.getData();
      }, 60 * 5 * 1000);
    },
    flowTrun(value) {
      var prefix_arr = ["K", "M", "G"];
      value = Math.round(value, 0);
      var i = 0;
      while (value > 1000) {
        value /= 1000;
        i++;
      }
      return Math.round(value, 0) + prefix_arr[i];
    }
  },
  destroyed() {
    clearTimeout(this.timer);
  },
  computed: {
  },
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
