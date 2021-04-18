const globalObj = {};

export const set = (key, value) => {
  globalObj[key] = value;
};

export const get = (key) => {
  return globalObj[key];
};
