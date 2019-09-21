import { Component, OnInit, Input } from '@angular/core';

import { CollectionStringMapperService } from 'app/core/core-services/collection-string-mapper.service';
import { isBaseIsAgendaItemContentObjectRepository } from 'app/core/repositories/base-is-agenda-item-content-object-repository';
import { ConfigService } from 'app/core/ui-services/config.service';
import { BaseSlideComponent } from 'app/slides/base-slide-component';
import { CommonListOfSpeakersSlideData } from './common-list-of-speakers-slide-data';
import { IBaseScaleScrollSlideComponent } from 'app/slides/base-scale-scroll-slide-component';

@Component({
    selector: 'os-common-list-of-speakers-slide',
    templateUrl: './common-list-of-speakers-slide.component.html',
    styleUrls: ['./common-list-of-speakers-slide.component.scss']
})
export class CommonListOfSpeakersSlideComponent extends BaseSlideComponent<CommonListOfSpeakersSlideData>
    implements OnInit, IBaseScaleScrollSlideComponent<CommonListOfSpeakersSlideData>  {
    /**
     * Boolean, whether the amount of speakers should be shown.
     */
    public hideAmountOfSpeakers: boolean;

    private _scroll = 0;

    @Input()
    public set scroll(value: number) {
        this._scroll = value;

        value *= -100;
        value += 40;
        this.textDivStyles['margin-top'] = `${value}px`;
    }

    public get scroll(): number {
        return this._scroll;
    }

    private _scale = 0;

    @Input()
    public set scale(value: number) {
        this._scale = value;

        value *= 10;
        value += 100;
        this.textDivStyles['font-size'] = `${value}%`;
    }

    public get scale(): number {
        return this._scale;
    }

    public textDivStyles: {
        'margin-top'?: string;
        'font-size'?: string;
    } = {};

    
    public constructor(
        private collectionStringMapperService: CollectionStringMapperService,
        private configService: ConfigService
    ) {
        super();
    }

    /**
     * OnInit-function.
     * Load the config for `agenda_hide_amount_of_speakers`.
     */
    public ngOnInit(): void {
        this.configService
            .get<boolean>('agenda_hide_amount_of_speakers')
            .subscribe(enabled => (this.hideAmountOfSpeakers = enabled));
    }

    public getTitle(): string {
        if (!this.data.data.content_object_collection || !this.data.data.title_information) {
            return '';
        }

        const repo = this.collectionStringMapperService.getRepository(this.data.data.content_object_collection);

        if (isBaseIsAgendaItemContentObjectRepository(repo)) {
            return repo.getAgendaSlideTitle(this.data.data.title_information);
        } else {
            throw new Error('The content object has no agenda base repository!');
        }
    }

    /**
     * @retuns the amount of waiting speakers
     */
    public getSpeakersCount(): number {
        if (this.data && this.data.data.waiting) {
            return this.data.data.waiting.length;
        }
        return 0;
    }


    public getSpeakerNameWithLinebreak(name: string): string[] {
        const indexStart = name.indexOf('(');
        const indexEnd = name.indexOf(')');
        let splittedName = [];
        if (indexStart > 0){
            // short name + structure level
            return [
                name.substring(0, indexStart),
                '('+name.substring(indexStart+1, indexEnd)+')'
            ];
        } else {
            return [name];
        }
    }
}
