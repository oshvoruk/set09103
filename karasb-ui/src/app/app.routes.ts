import { Routes } from '@angular/router';
import { Explore } from './explore/explore';
import { Layout } from './layout/layout';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'explore',
    pathMatch: 'full',
  },
  {
    path: '',
    component: Layout,
    children: [
      {
        path: 'explore',
        component: Explore,
      },
      {
        path: 'compare',
        component: Explore,
      },
      {
        path: 'about',
        component: Explore,
      },
    ],
  },
];
