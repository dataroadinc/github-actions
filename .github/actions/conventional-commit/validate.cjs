const {header_pattern: pattern} = require('./policy.json');

module.exports = function validateTitle(title) {
  if (typeof title !== 'string' || /[\r\n]/.test(title) || !new RegExp(pattern).test(title)) {
    throw new Error('Conventional Commit required: type(scope): description (optional ! for breaking changes)');
  }
  return title;
};
