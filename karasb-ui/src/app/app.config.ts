import { registerLocaleData } from '@angular/common';
import en from '@angular/common/locales/en';
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideMaplibreWorker } from '@maplibre/ngx-maplibre-gl/config';
import { provideNzDateFnsAdapter } from 'ng-zorro-antd/core/time';
import { en_GB, provideNzI18n } from 'ng-zorro-antd/i18n';
import { routes } from './app.routes';

registerLocaleData(en);

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideNzI18n(en_GB),
    provideNzDateFnsAdapter(),
    provideMaplibreWorker('maplibre-gl-worker.mjs')
  ],
};
