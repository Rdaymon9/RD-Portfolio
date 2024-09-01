Select *,
row_number() Over(
partition by company, industry, total_laid_off, percentage_laid_off, `date`) As row_num
From layoffs_staging;

With duplicate_cte As
(
Select *,
row_number() Over(
partition by company, location,
industry, total_laid_off, percentage_laid_off, `date`, stage
, country, funds_raised_millions) as row_num
From layoffs_staging
)
select *
from duplicate_cte
Where row_num > 1;

Select *
From layoffs_staging
Where company = 'oda';

CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num` Int
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

select *
from layoffs_staging2;

Insert into layoffs_staging2
Select *,
row_number() Over(
partition by company, location,
industry, total_laid_off, percentage_laid_off, `date`, stage
, country, funds_raised_millions) as row_num
From layoffs_staging;

Select *
From layoffs_staging2
Where row_num > 1;

Delete 
From layoffs_staging2
Where row_num > 1;

Select *
From layoffs_staging2;

Select company, trim(company)
From layoffs_staging2;

update layoffs_staging2
set company =  trim(company);

Select distinct industry
from layoffs_staging2
order by 1;

Select *
From layoffs_staging2
Where industry like 'crypto%';

update layoffs_staging2
set industry = 'crypto'
where industry like 'crypto%';

Select distinct industry
from layoffs_staging2
;

Select distinct country
from layoffs_staging2
order by 1;

Select *
From layoffs_staging2
Where country like 'united states%'
order by 1;

Select distinct country, trim(Trailing '.' From Country)
From layoffs_staging2
Order by 1;

Update layoffs_staging2
Set country = trim(Trailing '.' From Country)
Where country like 'United States%';

Select * From layoffs_staging2;

Select `date`
From layoffs_staging2;

Select `date`,
str_to_date(`date`, '%m/%d/%Y')
From layoffs_staging2;

Update layoffs_staging2
Set `date` = str_to_date(`date`, '%m/%d/%Y');

Alter table layoffs_staging2
Modify column `date` date;

Select * from layoffs_staging2;

Select *
From layoffs_staging2
Where total_laid_off is null
And percentage_laid_off is null;

Update layoffs_staging2
Set industry = null
Where Industry = ' ';

Select *
From layoffs_staging2
Where company = 'Airbnb';

Select *
From layoffs_staging2 t1
Join layoffs_staging2 t2
	On t1.company = t2.company
Where (t1.industry is null or t1.industry = ' ')
And t2.industry is not null;

Select t1.industy, t2.industry
From layoffs_staging2 t1
Join layoffs_staging2 t2
	On t1.company = t2.company
Where (t1.industry is null or t1.industry = ' ')
And t2.industry is not null;

Update layoffs_staging2 t1
Join layoffs_staging2 t2
	On t1.company = t2.company
Set t1.industry = t2.industry
Where t1.industry is null
And t2.industry is not null;

Select *
from layoffs_staging2
where company like 'Bally%';

Select *
From layoffs_staging2
Where total_laid_off is null
And percentage_laid_off is null;

Delete 
From layoffs_staging2
Where total_laid_off is null
And percentage_laid_off is null;

Select *
From layoffs_staging2;

Alter table layoffs_staging2
Drop Column row_num;