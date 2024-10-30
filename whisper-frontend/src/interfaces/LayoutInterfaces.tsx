import { ElementType, ReactNode } from 'react';

export interface HeaderLinkPropType {
  to: string;
  text: string;
}

export interface SidebarLinkPropType {
  to: string;
  text: string;
  isActive: boolean;
  Icon: ElementType;
}

export interface DoubleLayoutProps {
  firstChild: ReactNode;
  secondChild: ReactNode;
  firstChildHeader: ReactNode;
  secondChildHeader: ReactNode;
  showSecondChild: boolean;
  // onBackToList: () => void;
}

export interface LayoutProps {
  children: ReactNode;
}

export interface MainLayoutProps {
  children: ReactNode;
}

export interface SingleLayoutProps {
  children: ReactNode;
}
