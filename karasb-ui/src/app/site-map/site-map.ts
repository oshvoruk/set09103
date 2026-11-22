import { httpResource } from '@angular/common/http';
import { Component, computed, isDevMode } from '@angular/core';
import { NgxMapLibreGLModule } from '@maplibre/ngx-maplibre-gl';
import { LngLatBounds } from 'maplibre-gl';
import { NzResultComponent } from 'ng-zorro-antd/result';

interface Site {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  watercourse: string;
}

@Component({
  imports: [NgxMapLibreGLModule, NzResultComponent],
  selector: 'app-site-map',
  styleUrl: './site-map.css',
  templateUrl: './site-map.html',
})
export class SiteMap {
  protected readonly mapStyle = isDevMode()
    ? '/styles/site-map.json'
    : '/static/styles/site-map.json';

  protected readonly sites = httpResource<Site[]>(() => '/api/sites', { defaultValue: [] });

  protected readonly bounds = computed<LngLatBounds | undefined>(() => {
    const sites = this.sites.value();

    return sites.length
      ? sites.reduce(
          (bounds, site) => bounds.extend([site.longitude, site.latitude]),
          new LngLatBounds(),
        )
      : undefined;
  });
}
