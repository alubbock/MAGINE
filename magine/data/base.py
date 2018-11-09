import numpy as np
import pandas as pd

from magine.plotting.heatmaps import heatmap_from_array


class BaseData(pd.DataFrame):
    _index = None

    def __init__(self, *args, **kwargs):
        super(BaseData, self).__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return BaseData

    def pivoter(self, convert_to_log, columns, values, index=None,
                fill_value=None, min_sig=0):
        """ Pivot data on provided axis.

        Parameters
        ----------
        convert_to_log : bool
            Convert values column to log2
        index : str
            Index for pivot table
        columns : str
            Columns to pivot
        values : str
            Values of pivot table
        fill_value : float, optional
            Fill pivot table nans with
        min_sig : int
            Required number of significant terms to keep in a row, default 0

        Returns
        -------

        """
        d_copy = self.copy()
        if index is None:
            index = self._index

        if convert_to_log:
            d_copy.log2_normalize_df(values, inplace=True)

        if min_sig:
            assert isinstance(min_sig, int)
            if 'significant' not in d_copy.columns:
                print('In order to filter based on minimum sig figs, '
                      'please add a column of signficant terms with '
                      'a tag of "significant"')

            d_copy.filter_by_minimum_sig_columns(index=index, columns=columns,
                                                 min_terms=min_sig,
                                                 inplace=True)

        array = pd.pivot_table(d_copy, index=index, fill_value=fill_value,
                               columns=columns, values=values)

        if isinstance(columns, list):
            x = sorted(tuple(map(tuple, d_copy[columns].values)))
            array.sort_values(by=x, ascending=False, inplace=True)
        elif isinstance(columns, str):
            array.sort_values(by=list(sorted(d_copy[columns].unique())),
                              ascending=False, inplace=True)
        return array

    def filter_by_minimum_sig_columns(self, columns='sample_id', index=None,
                                      min_terms=3, inplace=False):
        """ Filter index to have at least "min_terms" significant species.

        Parameters
        ----------
        columns : str
            Columns to consider
        index : str, list
            The column with which to filter by counts
        min_terms : int
            Number of terms required to not be filtered
        inplace : bool
            Filter in place or return a copy of the filtered data

        Returns
        -------
        new_data : BaseData
        """
        if index is None:
            index = self._index
        # create safe copy of array
        new_data = self.copy()

        # get list of columns
        cols_to_check = list(new_data[columns].unique())
        if 'significant' in new_data.columns:
            flag = 'significant'
        elif 'significant_flag' in new_data.columns:
            flag = 'significant_flag'
        else:
            flag = None
        assert flag in new_data.columns, 'Requires significant_flag column'
        # pivot
        sig = pd.pivot_table(new_data,
                             index=index,
                             fill_value=0,
                             values=flag,
                             columns=columns
                             )[cols_to_check]

        # convert everything thats not 0 to 1
        sig[sig > 0] = 1
        sig = sig[sig.T.sum() >= min_terms]
        if isinstance(index, list):
            keepers = {i[0] for i in sig.index.values}
            new_data = new_data[new_data[index[0]].isin(keepers)]
        elif isinstance(index, str):
            keepers = {i for i in sig.index.values}
            new_data = new_data.loc[new_data[index].isin(keepers)]
        else:
            print("Index is not a str or a list. What is it?")

        if inplace:
            self._update_inplace(new_data)
        else:
            return new_data

    def log2_normalize_df(self, column='fold_change', inplace=False):
        """ Convert "fold_change" column to log2.

        Does so by taking log2 of all positive values and -log2 of all negative
        values.

        Parameters
        ----------
        column : str
            Column to convert
        inplace : bool
            Where to apply log2 in place or return new dataframe

        Returns
        -------

        """
        new_data = self.copy()
        greater = new_data[column] > 0
        less = new_data[column] < 0
        new_data.loc[greater, column] = np.log2(new_data[greater][column])
        new_data.loc[less, column] = -np.log2(-new_data[less][column])
        if inplace:
            self._update_inplace(new_data)
        else:
            return new_data

    def heatmap(self, subset_list=None, convert_to_log=True,
                y_tick_labels='auto',
                cluster_row=False, cluster_col=False, cluster_by_set=False,
                index=None, values=None, columns=None,
                annotate_sig=True, figsize=(8, 12), div_colors=True,
                linewidths=0, num_colors=21, rank_index=False):
        """ Creates heatmap of data, providing pivot and formatting.

        Parameters
        ----------
        subset_list : list
            List for index to subset
        convert_to_log : bool
            Convert values to log2 scale
        y_tick_labels : str
            Column of values, default = 'auto'
        cluster_row : bool
        cluster_col : bool
        cluster_by_set : bool
            Clusters by gene set, only used in EnrichmentResult derived class
        index : str
            Index of heatmap, will be 'row' variables
        values : str
            Values to display in heatmap
        columns : str
            Value that will be used as columns
        annotate_sig : bool
            Add '*' annotation to not 'significant=True' column
        figsize : tuple
            Figure size to pass to matplotlib
        div_colors : bool
            Use colors that are divergent
            (red to blue, instead of shades of blue)
        num_colors : int
            How many colors to include on color bar
        linewidths : float
            line width between individual cols and rows
        rank_index : bool
            Rank index alphabetically

        Returns
        -------
        matplotlib.figure

        """

        if index is None:
            index = self._identifier
        if values is None:
            values = self._value_name
        if columns is None:
            columns = self._sample_id_name

        if subset_list is not None:
            df_copy = self.copy()
            df_copy = df_copy.loc[df_copy[index].isin(subset_list)]
        else:
            df_copy = self.copy()
        return heatmap_from_array(
            df_copy, convert_to_log=convert_to_log,
            y_tick_labels=y_tick_labels,
            cluster_row=cluster_row, cluster_col=cluster_col,
            cluster_by_set=cluster_by_set,  figsize=figsize,
            columns=columns, index=index, values=values,
            div_colors=div_colors, num_colors=num_colors,
            rank_index=rank_index, annotate_sig=annotate_sig,
            linewidths=linewidths,
        )