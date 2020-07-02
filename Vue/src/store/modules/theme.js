// 设置文件
import setting from '@/settings.js'
// import store from './store'
export default {
  namespaced: true,
  state: {
    // 主题
    list: setting.theme.list,
    // 现在激活的主题 这应该是一个名字 不是对象
    activeName: setting.theme.list[0].name
  },
  getters: {
    /**
     * @description 返回当前的主题信息 不是一个名字 而是当前激活主题的所有数据
     * @param {Object} state state
     */
    activeSetting (state) {
      console.log("我跳到这里了",state.list.find(theme => theme.name === state.activeName))
      return state.list.find(theme => theme.name === state.activeName)
    }
  },
  actions: {
    /**
     * @description 激活一个主题
     * @param {String} themeValue 需要激活的主题名称
     */
    set ({ state, commit, dispatch }, themeName) {
      return new Promise(async resolve => {
        // 检查这个主题在主题列表里是否存在
        state.activeName = state.list.find(e => e.name === themeName) ? themeName : state.list[0].name
        // 将 vuex 中的主题应用到 dom
        commit('dom')
        console.log(state.activeName)
        // 持久化
        await dispatch('user/setUserTheme',state.activeName,{root:true})
        resolve()
      })
    },
    /**
     * @description 从持久化数据加载主题设置     * @param {Object} context
     */
    load ({ state, commit,dispatch },name) {
      return new Promise(async resolve => {
        // store 赋值
        let activeName=localStorage.getItem(name+"Theme")
        // 检查这个主题在主题列表里是否存在

        if (state.list.find(e => e.name === activeName)) {
          state.activeName = activeName
        } else {
          state.activeName = state.list[0].name
          // 持久化
          await dispatch('user/setUserTheme',state.activeName,{root:true})
        }
        // 将 vuex 中的主题应用到 dom
        commit('dom')
        // end
        resolve()
      })
    }
  },
  mutations: {
    /**
     * @description 将 vuex 中的主题应用到 dom
     * @param {Object} state state
     */
    dom (state) {
      document.body.className = `theme-${state.activeName}`
    }
  }
}
// console.log(state.list);
