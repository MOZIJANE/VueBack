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
    // idDict: {
    //   type: Array,
    //   default: () => {}
    // },
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
        this.timer();
      },
      deep: true //对象内部属性的监听，关键。n
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
          trigger: "item",
          triggerOn:'mousemove',
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
    },
    getData() {

      this.x +=1;
      this.$request({
        url: "/api/getSankeyFromUrl/",
        method: "get",
      }).then(res => {
        if(res.data){
          this.option.series=[]
          var links = res.data["NetFlow"]["links"]
          var nodes = res.data["NetFlow"]["nodes"]
          var yuan_list = []
          for(var ke in links){
            var list1 = {source:links[ke]["source"],target:links[ke]["target"]}
            yuan_list.push(list1)
          }
          console.log(JSON.stringify(yuan_list))
          var rm_list =[]
          for(var ke1 in yuan_list){
            var re_list = {source:yuan_list[ke1]["target"],target:yuan_list[ke1]["source"]}
            if(JSON.stringify(yuan_list).indexOf(JSON.stringify(re_list)) > -1){
              rm_list.push(links[ke1])
              console.log(JSON.stringify(links[ke1]))
              console.log(JSON.stringify(yuan_list[ke1]))
              console.log("_____________________________________________")
            }
          }

          console.log(rm_list)
          for(var re in rm_list){
            links.splice(rm_list[re],1)
          }
          console.log(links)
          var sankey={
            "type": "sankey",
            data:res.data["NetFlow"].nodes,
            links:links,
            focusNodeAdjacency: 'allEdges',
            itemStyle: {
                  borderWidth: 1,
                  borderColor: '#aaa'
              },
              lineStyle: {
                  color: 'source',
                  curveness: 0.5
              }
          }
            this.option.series.push(sankey)
        }
        this.initChart();
      });
    },
    timer() {
      return setTimeout(() => {
        this.getData();
      }, 5 * 60 * 1000);
    }
  },
  destroyed() {
    clearTimeout(this.timer);
  }
};
</script>