const path = require('path');

module.exports = {
  mode: "development",
  entry: {
      main : './app/static/js/main.js',
      profile: './app/static/js/profile.js',
      questions_detail: './app/static/js/question_detail.js',
      questions: './app/static/js/questions.js',
      user: './app/static/js/user.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, '../app/static/js/dist')
  }
};