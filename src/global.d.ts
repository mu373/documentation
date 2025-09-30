/// <reference types="@docusaurus/module-type-aliases" />

declare module '*.module.scss' {
  const classes: {readonly [key: string]: string};
  export default classes;
}
