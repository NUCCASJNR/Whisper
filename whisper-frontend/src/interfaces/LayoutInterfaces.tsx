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

export interface MainLayoutProps {
  children: ReactNode;
}
