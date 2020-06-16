<template>
  <div :class="className" :id="id" :style="{height:height,width:width}" />
</template>
 
<script>
import echarts from "echarts";
import { timeComputed } from "@/utils/validate";
// import { EleResize } from "@/assets/js/esresize";
// import { ToseriesLine } from "@/assets/js/seriesLine";

export default {
  props: {
    className: {
      type: String,
      default: "chart"
    },
    id: {
      type: String,
      default: "chart"
    },
    idDict: {
      type: Array,
      default: () => {}
    },
    width: {
      type: String,
      default: "100%"
    },
    height: {
      type: String,
      default: "23.4rem"
    },
    title: {
      type: String,
      default: "title"
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
      x:0, //watch监听chartData有问题，因此用x
      chartData: {},
      option: {
        title: {
          text: this.title,
          x:'center',
          textStyle:{
            fontSize: 17,
            color:'#000',
            fontWeight: 'normal'
          }
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            animation: false
          },
          formatter: function (params, ticket, callback) {
              //图表title名称
              var seriesName = params[0].seriesName
              //值
              var value = params[0].value
              // console.log(typeof value)
              var valueFliter=(value,index)=>{return `${value[0].replace("T"," ")}  ${value[1]}ms`}
              return seriesName + '<br />' + valueFliter(value)
          }
        },
        legend: {//图例组件，颜色和名字
          right:'10%',
          top:'10%',
          itemGap: 16,
          itemWidth: 18,
          itemHeight: 10,
          data:'',
              //icon:'image://../wwwroot/js/url2.png', //路径
          textStyle: {
          color: '#a8aab0',
          fontStyle: 'normal',
          fontFamily: '微软雅黑',
          fontSize: 12,            
          }
        },
        xAxis: {
          name: '时间',
          type: "time",
          splitLine: {
            show: false
          }
        },
        yAxis: {
          name: '延迟',
          type: "value",
          boundaryGap: [0, "100%"],
          splitLine: {
            show: false
          }
        },
        series: []
      }
    };
  },
  created() {
    this.getData();
  },
  mounted() {
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart() {
      if(this.chart){
        this.chart.setOption(this.option);
      }else{
        this.chart = echarts.init(document.getElementById(this.id));

        this.chart.setOption(this.option);
      }
      
      window.addEventListener("resize", this.chart.resize);
      // EleResize.on(this.chart, listener)
    },
    getData() {
      var dateTime = timeComputed(60);
      // console.log(this.idDict);
      this.x +=1;
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
        if(res.data){
          this.option.series=[]
          // console.log(res.data)
          for(var ke in res.data){
            var line={
              "name": "",
              "type": "line",
              "showSymbol": false,
              "hoverAnimation": false,
              "data": "",
              "areaStyle": {
                "normal": {
                  "color": "#d4f8e8" //改变区域颜色
                }
              },
              "itemStyle": {
                "normal": {
                  "color": "#ffa34d", //改变折线点的颜色
                  "lineStyle": {
                    "color": "#ffa34d" //改变折线颜色
                  }
                }
              }
            }
            line.name = ke
            // console.log(line.name)
            // console.log(this.series[i])
            this.chartData[ke]=res.data[ke]
            // console.log(this.chartData[ke])
            line.data=this.chartData[ke]
            // console.log(series[i])
            this.option.series.push(line)
          }
        }
        this.initChart();
      });
    },
    timer() {
      return setTimeout(() => {
        this.getData();
      }, 60 *5* 1000);
    }
  },
  destroyed() {
    clearTimeout(this.timer);
  }
};
</script>