import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    roles: [],
    userImg:""
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_IMG: (state, img) =>{
    state.userImg = img
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        // console.log(response, data)
        commit('SET_TOKEN', data.token)
        setToken(data.token)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state,dispatch }) {
    return new Promise((resolve, reject) => {
      // console.log("store", state.token)
      getInfo(state.token).then(response => {
        const { data } = response
        console.log(data)
        if (!data) {
          reject('Verification failed, please Login again.')
        }
        const { name,roles } = data
        commit('SET_NAME', name)
        commit('SET_ROLES', roles)
        commit('SET_IMG', "http://172.22.254.20:10000"+data.profile_path[0])
        dispatch("theme/load",name,{root:true})
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  setUserTheme({ commit },theme){
    return new Promise((resolve, reject)=>{
      localStorage.setItem(state.name+"Theme",theme)
      resolve()
    })
  },

  setUserImg({commit},img){
    return new Promise((resolve)=>{
      commit('SET_IMG', "http://172.22.254.20:10000"+img)
      resolve()
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

