import React, {type ComponentProps, type ReactNode} from 'react';
import clsx from 'clsx';
import {ThemeClassNames, usePrismTheme} from '@docusaurus/theme-common';
import styles from './styles.module.scss';

export default function CodeBlockContainer<T extends 'div' | 'pre'>({
  as: As,
  ...props
}: {as: T} & ComponentProps<T>): ReactNode {
  const prismTheme = usePrismTheme();
  return (
    <As
      // Polymorphic components are hard to type, without `oneOf` generics
      {...(props as any)}
      className={clsx(
        props.className,
        styles.codeBlockContainer,
        ThemeClassNames.common.codeBlock,
      )}
    />
  );
}
