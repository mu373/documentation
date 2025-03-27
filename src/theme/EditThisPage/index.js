import React from 'react';
import Translate from '@docusaurus/Translate';
import {ThemeClassNames} from '@docusaurus/theme-common';
import Link from '@docusaurus/Link';
import { FaGithub } from 'react-icons/fa';

// The default is "edit this page" but we want to change it to "view source"
export default function ViewSourceOnGitHub(props) {

  // Get the editUrl from props (passed by Docusaurus)
  const {editUrl} = props;

  // console.log(props)

  if (!{editUrl}) {
    return null;
  }
  
  // Convert edit URL to view URL
  const viewSourceUrl = editUrl.replace('/edit/', '/blob/');
  
  return (
    <Link to={viewSourceUrl} className={ThemeClassNames.common.viewSource}>
      <FaGithub style={{ marginRight: '6px', marginBottom: '-0.12em' }} />
      <Translate
        id="theme.common.viewSource"
        description="The link label to view the source of the page">
        View source
      </Translate>
    </Link>
  );
}