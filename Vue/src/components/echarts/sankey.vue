<template>
  <div :style="{ height: height, width: width }" />
</template>

<script>
import resize from "./mixins/resize";

export default {
  mixins: [resize],
  props: {
    apiName: {
      type: String,
      default: "/api/getSankeyFromUrl_GZ_HK/"
    },
    width: {
      type: String,
      default: "100%"
    },
    height: {
      type: String,
      default: "23.4rem"
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
      x: 0, //watch监听chartData有问题，因此用x
      chartData: {},
      option: {
        // title: {
        //   text: this.title,
        //   x:'center',
        //   textStyle:{
        //     fontSize: 17,
        //     color:'#000',
        //     fontWeight: 'normal'
        //   }
        // },
        tooltip: {
          trigger: "item",
          triggerOn: "mousemove"
        },
        series: []
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
        this.chart = this.$echarts.init(this.$el);
        this.chart.setOption(this.option);
      }
    },
    getData() {
      this.x += 1;
      this.$request({
        url: this.apiName,
        method: "get"
      }).then(res => {
        if (res.data) {
          this.option.series = [];
          res.data["NetFlow"]["links"].forEach(item => {
            item.source=item.source.length>15?item.source.slice(0, 15) +"...":item.source;
            item.target=item.target.length>15?item.target.slice(0, 15) +"...":item.target;
          });
          res.data["NetFlow"]["nodes"].forEach(item => {
            item.name=item.name.length>15?item.name.slice(0, 15) +"...":item.name;
          });
          var links = res.data["NetFlow"]["links"]
          var nodes = res.data["NetFlow"]["nodes"]
          var sankey = {
            type: "sankey",
            data: nodes.slice(0, 17),
            links: links,
            focusNodeAdjacency: "allEdges",
            itemStyle: {
              borderWidth: 1,
              borderColor: "#aaa"
            },
            lineStyle: {
              color: "source",
              curveness: 0.5
            }
          };
          this.option.series.push(sankey);
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
