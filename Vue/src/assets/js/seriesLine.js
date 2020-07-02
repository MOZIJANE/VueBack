var lineTemplate = {
  "name": "",
  "type": "line",
  "showSymbol": false,
  "hoverAnimation": false,
  "data": "",
  "areaStyle": {
    "normal": {
      "color": "#091e3b" //改变区域颜色
    }
  },
  "itemStyle": {
    "normal": {
      "color": "#8cd5c2", //改变折线点的颜色
      "lineStyle": {
        "color": "#8cd5c2" //改变折线颜色
      }
    }
  }
}

export function ToseriesLine(idDict) {
  var result=[];
  for(var i=0;i<idDict.length;i++) {
    // lineTemplate['name']=i['name'];
    result.push(lineTemplate)
  }
  console.log("result",result)
  return result
}