import { Component, OnInit } from '@angular/core';
import { MatSnackBar, MatDialog } from '@angular/material';
import { Router, ActivatedRoute } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { TranslateService } from '@ngx-translate/core';

import { AgendaCsvExportService } from '../../services/agenda-csv-export.service';
import { AgendaFilterListService } from '../../services/agenda-filter-list.service';
import { AgendaPdfService } from '../../services/agenda-pdf.service';
import { ConfigService } from 'app/core/ui-services/config.service';
import { DurationService } from 'app/core/ui-services/duration.service';
import { Item } from 'app/shared/models/agenda/item';
import { ItemInfoDialogComponent } from '../item-info-dialog/item-info-dialog.component';
import { ItemRepositoryService } from 'app/core/repositories/agenda/item-repository.service';
import { ListViewBaseComponent } from 'app/site/base/list-view-base';
import { OperatorService } from 'app/core/core-services/operator.service';
import { PromptService } from 'app/core/ui-services/prompt.service';
import { PdfDocumentService } from 'app/core/ui-services/pdf-document.service';
import { ViewportService } from 'app/core/ui-services/viewport.service';
import { ViewItem } from '../../models/view-item';
import { ProjectorElementBuildDeskriptor } from 'app/site/base/projectable';
import { _ } from 'app/core/translate/translation-marker';

/**
 * List view for the agenda.
 */
@Component({
    selector: 'os-agenda-list',
    templateUrl: './agenda-list.component.html',
    styleUrls: ['./agenda-list.component.scss']
})
export class AgendaListComponent extends ListViewBaseComponent<ViewItem, Item> implements OnInit {
    /**
     * Determine the display columns in desktop view
     */
    public displayedColumnsDesktop: string[] = ['title', 'info', 'speakers'];

    /**
     * Determine the display columns in mobile view
     */
    public displayedColumnsMobile: string[] = ['title', 'speakers'];

    public isNumberingAllowed: boolean;

    /**
     * Helper to check main button permissions
     *
     * @returns true if the operator can manage agenda items
     */
    public get canManage(): boolean {
        return this.operator.hasPerms('agenda.can_manage');
    }

    public itemListSlide: ProjectorElementBuildDeskriptor = {
        getBasicProjectorElement: options => ({
            name: 'agenda/item-list',
            getIdentifiers: () => ['name']
        }),
        slideOptions: [
            {
                key: 'only_main_items',
                displayName: _('Only main agenda items'),
                default: false
            }
        ],
        projectionDefaultName: 'agenda_all_items',
        getDialogTitle: () => this.translate.instant('Agenda')
    };

    /**
     * The usual constructor for components
     * @param titleService Setting the browser tab title
     * @param translate translations
     * @param matSnackBar Shows errors and messages
     * @param operator The current user
     * @param route Angulars ActivatedRoute
     * @param router Angulars router
     * @param repo the agenda repository,
     * @param promptService the delete prompt
     * @param dialog to change info values
     * @param config read out config values
     * @param vp determine the viewport
     * @param durationService Converts numbers to readable duration strings
     * @param csvExport Handles the exporting into csv
     * @param filterService: service for filtering data
     * @param agendaPdfService: service for preparing a pdf of the agenda
     * @param pdfService: Service for exporting a pdf
     */
    public constructor(
        titleService: Title,
        protected translate: TranslateService, // protected required for ng-translate-extract
        matSnackBar: MatSnackBar,
        private operator: OperatorService,
        private route: ActivatedRoute,
        private router: Router,
        private repo: ItemRepositoryService,
        private promptService: PromptService,
        private dialog: MatDialog,
        private config: ConfigService,
        public vp: ViewportService,
        public durationService: DurationService,
        private csvExport: AgendaCsvExportService,
        public filterService: AgendaFilterListService,
        private agendaPdfService: AgendaPdfService,
        private pdfService: PdfDocumentService
    ) {
        super(titleService, translate, matSnackBar, filterService);

        // activate multiSelect mode for this listview
        this.canMultiSelect = true;
    }

    /**
     * Init function.
     * Sets the title, initializes the table and filter options, subscribes to filter service.
     */
    public ngOnInit(): void {
        super.setTitle('Agenda');
        this.initTable();
        this.config
            .get<boolean>('agenda_enable_numbering')
            .subscribe(autoNumbering => (this.isNumberingAllowed = autoNumbering));
        this.setFulltextFilter();
    }

    protected onFilter(): void {
        this.filterService.filter().subscribe(newAgendaItems => {
            newAgendaItems.sort((a, b) => a.agendaListWeight - b.agendaListWeight);
            this.dataSource.data = newAgendaItems;
            this.checkSelection();
        });
    }

    /**
     * Links to the content object.
     *
     * @param item the item that was selected from the list view
     */
    public singleSelectAction(item: ViewItem): void {
        if (item.contentObject) {
            this.router.navigate([item.contentObject.getDetailStateURL()]);
        }
    }

    /**
     * Opens the item-info-dialog.
     * Enable direct changing of various information
     *
     * @param item The view item that was clicked
     */
    public openEditInfo(item: ViewItem, event: MouseEvent): void {
        if (this.isMultiSelect || !this.canManage) {
            return;
        }
        event.stopPropagation();
        const dialogRef = this.dialog.open(ItemInfoDialogComponent, {
            width: '400px',
            data: item,
            disableClose: true
        });

        dialogRef.afterClosed().subscribe(result => {
            if (result) {
                if (result.durationText) {
                    result.duration = this.durationService.stringToDuration(result.durationText);
                } else {
                    result.duration = 0;
                }
                this.repo.update(result, item);
            }
        });
    }

    /**
     * Click handler for the numbering button to enable auto numbering
     */
    public async onAutoNumbering(): Promise<void> {
        const title = this.translate.instant('Are you sure you want to number all agenda items?');
        if (await this.promptService.open(title, null)) {
            await this.repo.autoNumbering().then(null, this.raiseError);
        }
    }

    /**
     * Click handler for the done button in the dot-menu
     */
    public async onDoneSingleButton(item: ViewItem): Promise<void> {
        await this.repo.update({ closed: !item.closed }, item).then(null, this.raiseError);
    }

    /**
     * Handler for the speakers button
     *
     * @param item indicates the row that was clicked on
     */
    public onSpeakerIcon(item: ViewItem, event: MouseEvent): void {
        event.stopPropagation();
        this.router.navigate([`${item.id}/speakers`], { relativeTo: this.route });
    }

    /**
     * Handler for the plus button.
     * Comes from the HeadBar Component
     */
    public onPlusButton(): void {
        this.router.navigate(['topics/new'], { relativeTo: this.route });
    }

    /**
     * Delete handler for a single item
     *
     * @param item The item to delete
     */
    public async onDelete(item: ViewItem): Promise<void> {
        const title = this.translate.instant('Are you sure you want to delete this entry?');
        const content = item.contentObject.getTitle();
        if (await this.promptService.open(title, content)) {
            await this.repo.delete(item).then(null, this.raiseError);
        }
    }

    /**
     * Handler for deleting multiple entries. Needs items in selectedRows, which
     * is only filled with any data in multiSelect mode
     */
    public async deleteSelected(): Promise<void> {
        const title = this.translate.instant('Are you sure you want to delete all selected items?');
        if (await this.promptService.open(title, null)) {
            for (const agenda of this.selectedRows) {
                await this.repo.delete(agenda);
            }
        }
    }

    /**
     * Sets multiple entries' open/closed state. Needs items in selectedRows, which
     * is only filled with any data in multiSelect mode
     *
     * @param closed true if the item is to be considered done
     */
    public async setClosedSelected(closed: boolean): Promise<void> {
        for (const agenda of this.selectedRows) {
            await this.repo.update({ closed: closed }, agenda);
        }
    }

    /**
     * Sets multiple entries' agenda type. Needs items in selectedRows, which
     * is only filled with any data in multiSelect mode.
     *
     * @param visible true if the item is to be shown
     */
    public async setAgendaType(agendaType: number): Promise<void> {
        for (const agenda of this.selectedRows) {
            await this.repo.update({ type: agendaType }, agenda).then(null, this.raiseError);
        }
    }

    /**
     * Determine what columns to show
     *
     * @returns an array of strings with the dialogs to show
     */
    public getColumnDefinition(): string[] {
        let columns = this.vp.isMobile ? this.displayedColumnsMobile : this.displayedColumnsDesktop;
        if (this.operator.hasPerms('agenda.can_manage')) {
            columns = columns.concat(['menu']);
        }
        if (this.operator.hasPerms('core.can_manage_projector') && !this.isMultiSelect) {
            columns = ['projector'].concat(columns);
        }
        if (this.isMultiSelect) {
            columns = ['selector'].concat(columns);
        }
        return columns;
    }

    /**
     * Export all items as CSV
     */
    public csvExportItemList(): void {
        this.csvExport.exportItemList(this.dataSource.filteredData);
    }

    /**
     * Triggers the export of the agenda. Currently filtered items and 'hidden'
     * items will not be exported
     */
    public onDownloadPdf(): void {
        const filename = this.translate.instant('Agenda');
        this.pdfService.download(this.agendaPdfService.agendaListToDocDef(this.dataSource.filteredData), filename);
    }

    /**
     * Get the calculated end date and time
     *
     * @returns a readable string with end date and time in the current languages' convention
     */
    public getDurationEndString(): string {
        const duration = this.repo.calculateDuration();
        if (!duration) {
            return '';
        }
        const durationString = this.durationService.durationToString(duration, 'h');
        const endTime = this.repo.calculateEndTime();
        const result = `${this.translate.instant('Duration')}: ${durationString}`;
        if (endTime) {
            return (
                result +
                ` (${this.translate.instant('Estimated end')}:
            ${endTime.toLocaleTimeString(this.translate.currentLang, { hour: 'numeric', minute: 'numeric' })} h)`
            );
        } else {
            return result;
        }
    }

    /**
     * Overwrites the dataSource's string filter with a case-insensitive search
     * in the item number and title
     */
    private setFulltextFilter(): void {
        this.dataSource.filterPredicate = (data, filter) => {
            if (!data) {
                return false;
            }
            filter = filter ? filter.toLowerCase() : '';
            return (
                data.itemNumber.toLowerCase().includes(filter) ||
                data
                    .getListTitle()
                    .toLowerCase()
                    .includes(filter)
            );
        };
    }
}
