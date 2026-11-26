import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NzGridModule } from 'ng-zorro-antd/grid';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzLayoutModule } from 'ng-zorro-antd/layout';
import { NzMenuModule } from 'ng-zorro-antd/menu';

@Component({
  imports: [NzLayoutModule, NzMenuModule, NzGridModule, NzInputModule, RouterModule],
  selector: 'app-navigation',
  styleUrl: './navigation.less',
  templateUrl: './navigation.html',
})
export class Navigation {}
