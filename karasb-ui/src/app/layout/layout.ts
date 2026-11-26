import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NzLayoutModule } from 'ng-zorro-antd/layout';
import { Navigation } from '../navigation/navigation';

@Component({
  imports: [Navigation, NzLayoutModule, RouterOutlet],
  selector: 'app-layout',
  styleUrl: './layout.less',
  templateUrl: './layout.html',
})
export class Layout {}
