import React, {type ComponentProps} from 'react';
import clsx from 'clsx';
import OriginalCodeBlockContainer from '@theme-original/CodeBlock/Container';

import styles from './styles.module.scss';

export default function CodeBlockContainer<T extends 'div' | 'pre'>({
  className,
  ...props
}: {as: T} & ComponentProps<T>) {
  return (
    <OriginalCodeBlockContainer
      {...props}
      className={clsx(styles.codeBlockContainer, className)}
    />
  );
}
