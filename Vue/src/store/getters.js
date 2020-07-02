const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  roles: state => state.user.roles,
  name: state => state.user.name,
  userImg: state => state.user.userImg,
  list: state => state.theme.list,
}
export default getters
