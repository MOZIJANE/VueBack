<template>
  <div />
</template>

<script>
import resize from "./mixins/resize";

export default {
  mixins: [resize],
  props: {
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
      deep: true //对象内部属性的监听，关键。n
    }
  },
  data() {
    return {
      chart: null,
      x: 0, //watch监听chartData有问题，因此用x
      chartData: [],
      opt: {
        index: 0
      },
      color: ["#FC619D", "#FF904D", "#48BFE3"],
      option: {
        baseOption: {
          grid: {
            top: 0,
            bottom: -15,
            right: 0,
            left: -100,
            containLabel: true
          },
          xAxis: {
            show: false
          },
          yAxis: [
            {
              triggerEvent: true,
              show: true,
              inverse: true,
              data: this.getArrByKey(this.chartData, "name"),
              fontSize: 16,
              axisLine: {
                show: false
              },
              splitLine: {
                show: false
              },
              axisTick: {
                show: false
              },
              axisLabel: {
                interval: 0,
                // color: "#000",
                align: "left",
                margin: 140,
                fontSize: 14,
                formatter: (value, index) => {
                  if (this.opt.index === 0 && index < 3) {
                    return (
                      "{idx" +
                      index +
                      "|" +
                      (1 + index) +
                      "} {title|" +
                      value +
                      "}"
                    );
                  } else if (
                    this.opt.index !== 0 &&
                    index + this.opt.index < 9
                  ) {
                    return (
                      "{idx|0" +
                      (1 + index + this.opt.index) +
                      "} {title|" +
                      value +
                      "}"
                    );
                  } else {
                    return (
                      "{idx|" +
                      (1 + index + this.opt.index) +
                      "} {title|" +
                      value +
                      "}"
                    );
                  }
                },
                rich: {
                  idx0: {
                    color: "#FB375E",
                    backgroundColor: "#FFE8EC",
                    borderRadius: 100,
                    padding: [5, 8],
                    fontSize: 14
                  },
                  idx1: {
                    color: "#FF9023",
                    backgroundColor: "#FFEACF",
                    borderRadius: 100,
                    padding: [5, 8],
                    fontSize: 14
                  },
                  idx2: {
                    color: "#00FF00",
                    backgroundColor: "#E1F7F3",
                    borderRadius: 100,
                    padding: [5, 8],
                    fontSize: 14
                  },
                  idx: {
                    // color: "#000",
                    borderRadius: 100,
                    padding: [5, 8],
                    fontSize: 14
                  },
                  title: {
                    width: 180,
                    fontSize: 14
                  }
                }
              }
            },
            {
              triggerEvent: true,
              show: true,
              inverse: true,
              data: this.getArrByKey(this.chartData, "name"),
              axisLine: {
                show: false
              },
              splitLine: {
                show: false
              },
              axisTick: {
                show: false
              }
            }
          ],
          series: [
            {
              name: "条",
              type: "bar",
              yAxisIndex: 0,
              data: this.chartData,
              barWidth: 14,
              itemStyle: {
                color: val => {
                  if (val.dataIndex < 3 && this.opt.index === 0) {
                    return this.color[val.dataIndex];
                  } else {
                    return "#1990FF";
                  }
                },
                barBorderRadius: 30
              }
            }
          ]
        },
        media: [
          {
            query: {
              maxWidth: 567
            },
            option: {
              yAxis: [
                {
                },
                {
                  axisLabel: {
                    interval: 0,
                    // color: "#000",
                    align: "left",
                    margin: 10,
                    fontSize: 14,
                    formatter: (value, index) => {
                      return (
                        this.chartData[index].value + "%"
                      );
                    }
                  }
                }
              ]
            }
          },
          {
            option: {
              yAxis: [
                {},
                {
                  axisLabel: {
                    interval: 0,
                    // color: "#000",
                    align: "left",
                    margin: 20,
                    fontSize: 14,
                    formatter: (value, index) => {
                      return (
                        this.chartData[index].value+"%\tPort:" +
                        this.chartData[index].port
                      );
                    }
                  }
                }
              ]
            }
          }
        ]
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
        this.chart = this.$echarts.init(this.$el, "green");
        this.chart.setOption(this.option);
      }
    },
    getData() {
      this.x += 1;
      this.chartData = [];
      this.$request({
        url: "/api/getSankeyFromUrl/",
        method: "post",
        data: {"idDict":this.idDict}
      }).then(res => {
        if (res.data) {
          var links = res.data["NetFlow"]["links"].slice(0, 10);
          links.forEach(item => {
            item.source =
              item.source.length > 13
                ? item.source.slice(0, 9) + ".."
                : item.source;
            this.chartData.push({
              name: item.source,
              value: item.value,
              port: item.port
            });
          });
          this.chartData = this.chartData.sort((a, b) => {
            return b.value - a.value;
          });
          this.option.baseOption.series[0]["data"] = this.chartData;
          this.option.baseOption.yAxis[0]["data"] = this.getArrByKey(
            this.chartData,
            "name"
          );
          this.option.baseOption.yAxis[1]["data"] = this.getArrByKey(
            this.chartData,
            "name"
          );
        }
        this.initChart();
      });
    },
    timer() {
      return setTimeout(() => {
        this.getData();
      }, 5 * 60 * 1000);
    },
    getArrByKey(data, k) {
      let key = k || "value";
      let res = [];
      if (data) {
        data.forEach(function(t) {
          res.push(t[key]);
        });
      }
      return res;
    }
  },
  destroyed() {
    clearTimeout(this.timer);
  }
};
</script>
<style lang="scss" scoped>
@media (min-width: 992px) {
  div {
    width: 100%;
    height: 300px;
  }
}
@media (max-width: 768px) {
  div {
    width: 100%;
    height: 250px;
  }
}
</style>
